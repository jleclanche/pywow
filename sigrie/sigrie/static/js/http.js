if (typeof(JSON) == "undefined") {
	JSON = {
		parse: function(text) {
			var ret = !(/[^,:{}\[\]0-9.\-+Eaeflnr-u \n\r\t]/.test(text.replace(/"(\\.|[^"\\])*"/g, ''))) && eval('(' + text + ')')
			if (!ret) throw new Error("Invalid JSON");
			return ret
		}
	}
}

httplib = {
	request: function(url, options) {
		if (typeof(url) == "string") url = new URL(url);
		
		var defaults = {
			"method": "get",           // "get" || "post" || "script"
			"query": {},               // GET or POST query data
			"success": function() {},  // Callback upon success
			"failure": function() {},  // Callback upon failure
			"content": "auto"          // Content type to treat the reply as. "auto" || "json" || "text" || "xml" || "js"
		}
		
		for (var key in defaults) {
			if (typeof(options[key]) == "undefined") options[key] = defaults[key];
		}
		if ((options.method == "get") || (options.method == "script")) url.merge("query", options.query);
		options["url"] = url
		if ((options.method == "get") && (options.content == "js") && (url.url.host != currentURL.url.host)) options.method = "script";
		
		if (options.method == "script") {
			var script = document.createElement("script")
			script.onload = function(event) {
				if (typeof(event) != "object") event = window.event;
				httplib.scriptLoaded(event, options)
			}
			script.onreadystatechange = function(event) {
				if (typeof(event) != "object") event = window.event;
				if ((script.readyState == "loaded") || (script.readyState == "complete")) httplib.scriptLoaded(event, options);
			}
			script.src = options.url.toString()
			document.documentElement.appendChild(script)
		}
		else {
			var xhr = httplib.XMLHttpRequest()
			xhr.options = options
			xhr.onreadystatechange = httplib.readyStateChange
			if ((options.content == "xml") && (typeof(xhr.overrideMimeType) == "function")) xhr.overrideMimeType("text/xml");
			
			xhr.open(options.method.toUpperCase(), url.toString(), true)
			
			if (options.method == "post") {
				xhr.send(url.serialize(url.query))
			}
			else {
				xhr.send("")
			}
		}
	},
	
	scriptLoaded: function(event, options) { // TODO: Possible error handling (Or timeout)
		var result = {}
		
		result.status = 200
		result.statusText = "LOADED"
		result.responseText = true
		result.response = true
		result.xhr = false
		result.url = options.url
		
		if (typeof(options.success) == "function") options.success(result);
		httplib.log("Successful request to " + options.url + " via <script> tag")
	},
	
	readyStateChange: function() {
		if (this.readyState == 4) {
			var result = {}
			
			result.status = this.status
			result.statusText = this.statusText
			result.responseText = this.responseText
			result.xhr = this
			result.url = this.options.url
			result.headers = httplib.parseHeaders(this.getAllResponseHeaders())
			
			if (this.status == 200) {
				if ((typeof(this.options.content) != "string") || (this.options.content == "auto")) {
					if (typeof(result.headers["Content-Type"]) != "string") result.headers["Content-Type"] = "text/plain";
					switch (result.headers["Content-Type"]) {
						case "application/json":
							this.options.content = "json"
							break
						case "application/xml":
						case "text/xml":
							this.options.content = "xml"
							break
						default:
							this.options.content = "text"
					}
				}
				
				if (this.options.content == "json") {
					var json = httplib.stripJSONP(this.responseText)
					try	{
						result.response = JSON.parse(json)
					}
					catch (ex) {
						try {
							result.response = eval("(" + json + ")")
						}
						catch (evalex) {
							if (typeof(this.options.failure) == "function") this.options.failure(result);
							httplib.log("Invalid JSON returned in request from " + this.options["url"] + " (Exceptions are '" + ex + "' and '" + evalex + "'):\n" + json)
							return
						}
					}
				}
				else if (this.options.content == "js") {
					try {
						result.response = eval(this.responseText)
					}
					catch (ex) {
						if (typeof(this.options.failure) == "function") this.options.failure(result);
						httplib.log("Invalid javascript returned in request from " + this.options["url"] + " (" + ex + ")\n" + this.responseText)
					}
				}
				else if (this.options.content == "xml") {
					result.response = this.responseXml
				}
				else {
					result.response = this.responseText
				}
				
				if (typeof(this.options.success) == "function") this.options.success(result);
				httplib.log("Successful request to " + this.options["url"])
			}
			else {
				if (typeof(this.options.failure) == "function") this.options.failure(result);
				httplib.log("Failed request to " + this.options["url"])
			}
		}
	},
	
	stripJSONP: function(json) {
		var match
		if (match = json.match(/^\s*([\w\d_\$]+)\(({[\s\S]*})\)[;\s]*$/i)) {
			json = match[2]
		}
		return json
	},
	
	parseHeaders: function(input) {
		var result = {}
		var match
		
		while (match = input.match(/^([\w\d\-\_]+): (.+)$/m)) {
			input = input.substr(match[0].length)
			result[match[1]] = match[2]
		}
		
		return result
	},
	
	XMLHttpRequest: function() {
		if (typeof(XMLHttpRequest) != "undefined") return new XMLHttpRequest();
		
		try { 
			return new ActiveXObject("Msxml2.XMLHTTP.6.0")
		}
		catch (e) {}
		try { 
			return new ActiveXObject("Msxml2.XMLHTTP.3.0")
		}
		catch (e) {}
		try { 
			return new ActiveXObject("Msxml2.XMLHTTP")
		}
		catch (e) {}
		
		throw new Error("Unsupported browser, XmlHttpRequest cannot be created")
	},
	
	log: function(text) {
		if ((typeof(console) != "undefined") && (typeof(console.log) == "function")) console.log(text);
	}
}