<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:include href="language.xsl"/>
<xsl:include href="item-utils.xsl"/>

<xsl:template match="itemTooltip">
<table cellspacing='0' cellpadding='0' border='0'><tr><td>
<div class='myTable'>
<xsl:call-template name="itemTooltipTemplate" />
</div>
</td></tr></table>
</xsl:template>

<xsl:template match="itemTooltip" mode="recurse">
<xsl:call-template name="itemTooltipTemplate" />
</xsl:template>

<xsl:template name="itemTooltipTemplate">
<xsl:apply-templates select="name" />
<xsl:apply-templates select="zoneBound" />
<xsl:apply-templates select="instanceBound" />
<xsl:apply-templates select="conjured" />
<xsl:apply-templates select="bonding" />
<xsl:apply-templates select="maxCount" />
<xsl:apply-templates select="startQuestId" />
<xsl:apply-templates select="equipData" />
<xsl:apply-templates select="damageData" />
<xsl:apply-templates select="armor" />
<xsl:apply-templates select="blockValue" />
<xsl:apply-templates select="bonusStrength" />
<xsl:apply-templates select="bonusAgility" />
<xsl:apply-templates select="bonusStamina" />
<xsl:apply-templates select="bonusIntellect" />
<xsl:apply-templates select="bonusSpirit" />
<xsl:apply-templates select="fireResist" />
<xsl:apply-templates select="natureResist" />
<xsl:apply-templates select="frostResist" />
<xsl:apply-templates select="shadowResist" />
<xsl:apply-templates select="arcaneResist" />
<xsl:apply-templates select="enchant" />
<xsl:apply-templates select="randomEnchantData"/>
<xsl:apply-templates select="socketData" />
<xsl:apply-templates select="gemProperties" />
<xsl:apply-templates select="durability" />
<xsl:apply-templates select="allowableRaces" />
<xsl:apply-templates select="allowableClasses" />
<xsl:apply-templates select="requiredLevel" />
<xsl:apply-templates select="requiredSkill" />
<xsl:apply-templates select="requiredAbility" />
<!-- pvp rank required -->
<!-- pvp medal required -->
<xsl:apply-templates select="requiredFaction" />
<xsl:apply-templates select="bonusDefenseSkillRating" />
<xsl:apply-templates select="bonusDodgeRating" />
<xsl:apply-templates select="bonusParryRating" />
<xsl:apply-templates select="bonusBlockRating" />
<xsl:apply-templates select="bonusHitMeleeRating" />
<xsl:apply-templates select="bonusHitRangedRating" />
<xsl:apply-templates select="bonusHitSpellRating" />
<xsl:apply-templates select="bonusCritMeleeRating" />
<xsl:apply-templates select="bonusCritRangedRating" />
<xsl:apply-templates select="bonusCritSpellRating" />
<xsl:apply-templates select="bonusHitTakenMeleeRating" />
<xsl:apply-templates select="bonusHitTakenRangedRating" />
<xsl:apply-templates select="bonusHitTakenSpellRating" />
<xsl:apply-templates select="bonusCritTakenMeleeRating" />
<xsl:apply-templates select="bonusCritTakenRangedRating" />
<xsl:apply-templates select="bonusCritTakenSpellRating" />
<xsl:apply-templates select="bonusHasteMeleeRating" />
<xsl:apply-templates select="bonusHasteRangedRating" />
<xsl:apply-templates select="bonusHasteSpellRating" />
<xsl:apply-templates select="bonusHitRating" />
<xsl:apply-templates select="bonusCritRating" />
<xsl:apply-templates select="bonusHitTakenRating" />
<xsl:apply-templates select="bonusCritTakenRating" />
<xsl:apply-templates select="bonusResilienceRating" />
<xsl:apply-templates select="bonusHasteRating" />
<xsl:apply-templates select="spellData" />
<xsl:apply-templates select="setData" />
<!-- cooldown -->
<xsl:apply-templates select="desc" />
</xsl:template>

<!-- name -->
<xsl:template match="name">
    <xsl:variable name="randomSuffix" select="concat(' ',../randomEnchantData/suffix)" />

    <xsl:choose>
        <xsl:when test="string-length($randomSuffix) &gt; 0">
            <xsl:choose>
                <xsl:when test="../overallQualityId = 5"><span class="myOrange myBold myItemName"><xsl:value-of select="current()" /><xsl:value-of select="$randomSuffix" /></span></xsl:when>
                <xsl:when test="../overallQualityId = 4"><span class="myPurple myBold myItemName"><xsl:value-of select="current()" /><xsl:value-of select="$randomSuffix" /></span></xsl:when>
                <xsl:when test="../overallQualityId = 3"><span class="myBlue myBold myItemName"><xsl:value-of select="current()" /><xsl:value-of select="$randomSuffix" /></span></xsl:when>
                <xsl:when test="../overallQualityId = 2"><span class="myGreen myBold myItemName"><xsl:value-of select="current()" /><xsl:value-of select="$randomSuffix" /></span></xsl:when>
                <xsl:when test="../overallQualityId = 1"><span class="myWhite myBold myItemName"><xsl:value-of select="current()" /><xsl:value-of select="$randomSuffix" /></span></xsl:when>
                <xsl:when test="../overallQualityId = 0"><span class="myGray myBold myItemName"><xsl:value-of select="current()" /><xsl:value-of select="$randomSuffix" /></span></xsl:when>
            </xsl:choose>
        </xsl:when>
        <xsl:otherwise>
            <xsl:choose>
                <xsl:when test="../overallQualityId = 5"><span class="myOrange myBold myItemName"><xsl:value-of select="current()" /></span></xsl:when>
                <xsl:when test="../overallQualityId = 4"><span class="myPurple myBold myItemName"><xsl:value-of select="current()" /></span></xsl:when>
                <xsl:when test="../overallQualityId = 3"><span class="myBlue myBold myItemName"><xsl:value-of select="current()" /></span></xsl:when>
                <xsl:when test="../overallQualityId = 2"><span class="myGreen myBold myItemName"><xsl:value-of select="current()" /></span></xsl:when>
                <xsl:when test="../overallQualityId = 1"><span class="myWhite myBold myItemName"><xsl:value-of select="current()" /></span></xsl:when>
                <xsl:when test="../overallQualityId = 0"><span class="myGray myBold myItemName"><xsl:value-of select="current()" /></span></xsl:when>
            </xsl:choose>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>
                
<!-- zone bound -->
<xsl:template match="zoneBound">
    <br /><xsl:value-of select="current()" />
</xsl:template>

<!-- instance bound -->
<xsl:template match="instanceBound">
    <br /><xsl:value-of select="current()" />
</xsl:template>

<!-- conjured -->
<xsl:template match="conjured"><br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.conjured']"/></xsl:template>

<!-- bonding -->
<xsl:template match="bonding">
    <xsl:choose>
        <xsl:when test="current() = 1"><br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.binds-pickup']"/></xsl:when>
        <xsl:when test="current() = 2"><br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.binds-equipped']"/></xsl:when>
        <xsl:when test="current() = 3"><br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.binds-used']"/></xsl:when>
        <xsl:when test="current() = 4 or current() = 5"><br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.quest-item']"/></xsl:when>
    </xsl:choose>
</xsl:template>

<!-- unique (max count) -->
<xsl:template match="maxCount">
	<xsl:choose>
		<xsl:when test="@uniqueEquippable"><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.unique-equipped']"/></xsl:when>
	    <xsl:when test="current() &gt; 0">
		    <br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.unique']"/><xsl:if test="current() &gt; 1">&#160;(<xsl:value-of select="current()" />)</xsl:if>
	    </xsl:when>
	</xsl:choose>
</xsl:template>

<!-- quest item -->
<xsl:template match="startQuestId">
    <xsl:if test="current() &gt; 0"><br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.begins-quest']"/></xsl:if>
</xsl:template>

<!-- equip slot -->
<xsl:template match="equipData">
    <xsl:choose>
        <!-- inventoryType 18 = Bag -->
        <xsl:when test="inventoryType = 18"><br />
            <xsl:value-of select="containerSlots" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.slot']"/>&#160;<xsl:value-of select="subclassName" />
        </xsl:when>
        <!-- inventoryType 0 = non equip type -->
        <xsl:when test="inventoryType != 0">
            <xsl:choose>
                <!-- classId 6 = Projectile -->
                <xsl:when test="../classId = 6"><br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.projectile']"/></xsl:when>
                <xsl:otherwise><br />
                    <xsl:call-template name="printInventoryType">
                        <xsl:with-param name="type" select="inventoryType" />
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:if test="subclassName">
                <span class='tooltipRight'><xsl:value-of select='subclassName' /></span>
            </xsl:if>
        </xsl:when>
    </xsl:choose>
</xsl:template>

<!-- weapon damage/speed/dps -->
<!-- WoW rounds total dps up, and truncates attack speed -->
<xsl:template match="damageData">
    <xsl:choose>
        <!-- classId 6 = Projectile -->
        <!-- we're assuming here that projectiles don't have more than one damage type -->
        <xsl:when test="../classId = 6"><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.adds']"/>&#160;<xsl:value-of select="(damage[1]/min + damage[1]/max) * 0.5" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.dps']"/></xsl:when>
        <xsl:otherwise>
            <xsl:for-each select="damage">
                <xsl:choose>
                    <xsl:when test="position() = 1"><br />
                        <xsl:call-template name="printDamageType">
                            <xsl:with-param name="min" select="min" />
                            <xsl:with-param name="max" select="max" />
                            <xsl:with-param name="type" select="type" />
                        </xsl:call-template>
                        <xsl:if test="../speed"><span class='tooltipRight'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.speed']"/>&#160;<xsl:value-of select="format-number(floor(../speed * 100) div 100, '#.00')" /></span></xsl:if>
                    </xsl:when>
                    <xsl:otherwise><br />+ <xsl:call-template name="printDamageType">
                            <xsl:with-param name="min" select="min" />
                            <xsl:with-param name="max" select="max" />
                            <xsl:with-param name="type" select="type" />
                        </xsl:call-template>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
            <xsl:if test="dps"><br />(<xsl:value-of select="format-number(dps, '#.0')" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.dps']"/>)</xsl:if>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template name="printDamageType">
    <xsl:param name="min" />
    <xsl:param name="max" />
    <xsl:param name="type" />
    <xsl:choose>
        <xsl:when test="$type = 0"><xsl:value-of select="$min" /><xsl:if test="$max &gt; $min">-<xsl:value-of select="$max" /></xsl:if>&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.damage']"/></xsl:when>
        <xsl:when test="$type = 1"><xsl:value-of select="$min" /><xsl:if test="$max &gt; $min">-<xsl:value-of select="$max" /></xsl:if>&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.holy-damage']"/></xsl:when>
        <xsl:when test="$type = 2"><xsl:value-of select="$min" /><xsl:if test="$max &gt; $min">-<xsl:value-of select="$max" /></xsl:if>&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.fire-damage']"/></xsl:when>
        <xsl:when test="$type = 3"><xsl:value-of select="$min" /><xsl:if test="$max &gt; $min">-<xsl:value-of select="$max" /></xsl:if>&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.nature-damage']"/></xsl:when>
        <xsl:when test="$type = 4"><xsl:value-of select="$min" /><xsl:if test="$max &gt; $min">-<xsl:value-of select="$max" /></xsl:if>&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.frost-damage']"/></xsl:when>
        <xsl:when test="$type = 5"><xsl:value-of select="$min" /><xsl:if test="$max &gt; $min">-<xsl:value-of select="$max" /></xsl:if>&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.shadow-damage']"/></xsl:when>
        <xsl:when test="$type = 6"><xsl:value-of select="$min" /><xsl:if test="$max &gt; $min">-<xsl:value-of select="$max" /></xsl:if>&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.arcane-damage']"/></xsl:when>
    </xsl:choose>
</xsl:template>


<!-- armor -->
<xsl:template match="armor">
    <xsl:if test="current() &gt; 0"><br /><xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.armor']"/></xsl:if>
</xsl:template>

<!-- block value -->
<xsl:template match="blockValue">
    <xsl:if test="current() &gt; 0"><br /><xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.block']"/></xsl:if>
</xsl:template>

<!-- stat modifiers -->
<xsl:template match="bonusStrength">
    <xsl:choose>
        <xsl:when test="current() &lt; 0"><br />-<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.strength']"/></xsl:when>
        <xsl:when test="current() &gt; 0"><br />+<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.strength']"/></xsl:when>
    </xsl:choose>
</xsl:template>
<xsl:template match="bonusAgility">
    <xsl:choose>
        <xsl:when test="current() &lt; 0"><br />-<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.agility']"/></xsl:when>
        <xsl:when test="current() &gt; 0"><br />+<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.agility']"/></xsl:when>
    </xsl:choose>
</xsl:template>
<xsl:template match="bonusStamina">
    <xsl:choose>
        <xsl:when test="current() &lt; 0"><br />-<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.stamina']"/></xsl:when>
        <xsl:when test="current() &gt; 0"><br />+<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.stamina']"/></xsl:when>
    </xsl:choose>
</xsl:template>
<xsl:template match="bonusIntellect">
    <xsl:choose>
        <xsl:when test="current() &lt; 0"><br />-<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.intellect']"/></xsl:when>
        <xsl:when test="current() &gt; 0"><br />+<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.intellect']"/></xsl:when>
    </xsl:choose>
</xsl:template>
<xsl:template match="bonusSpirit">
    <xsl:choose>
        <xsl:when test="current() &lt; 0"><br />-<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.spirit']"/></xsl:when>
        <xsl:when test="current() &gt; 0"><br />+<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.spirit']"/></xsl:when>
    </xsl:choose>
</xsl:template>
    
<!-- resistances -->
<xsl:template match="fireResist">
    <xsl:choose>
        <xsl:when test="current() &lt; 0"><br />-<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.fire-resistance']"/></xsl:when>
        <xsl:when test="current() &gt; 0"><br />+<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.fire-resistance']"/></xsl:when>
    </xsl:choose>
</xsl:template>
<xsl:template match="natureResist">
    <xsl:choose>
        <xsl:when test="current() &lt; 0"><br />-<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.nature-resistance']"/></xsl:when>
        <xsl:when test="current() &gt; 0"><br />+<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.nature-resistance']"/></xsl:when>
    </xsl:choose>
</xsl:template>
<xsl:template match="frostResist">
    <xsl:choose>
        <xsl:when test="current() &lt; 0"><br />-<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.frost-resistance']"/></xsl:when>
        <xsl:when test="current() &gt; 0"><br />+<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.frost-resistance']"/></xsl:when>
    </xsl:choose>
</xsl:template>
<xsl:template match="shadowResist">
    <xsl:choose>
        <xsl:when test="current() &lt; 0"><br />-<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.shadow-resistance']"/></xsl:when>
        <xsl:when test="current() &gt; 0"><br />+<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.shadow-resistance']"/></xsl:when>
    </xsl:choose>
</xsl:template>
<xsl:template match="arcaneResist">
    <xsl:choose>
        <xsl:when test="current() &lt; 0"><br />-<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.arcane-resistance']"/></xsl:when>
        <xsl:when test="current() &gt; 0"><br />+<xsl:value-of select="current()" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.arcane-resistance']"/></xsl:when>
    </xsl:choose>
</xsl:template>
    
<!-- enchantments -->
<xsl:template match="enchant"><br /><span class="bonusGreen"><xsl:value-of select="current()" /></span>
</xsl:template>

<xsl:template match="socketData">
	<xsl:variable name="numGemsMatched" select="count(socket/@match)" />

    <xsl:for-each select="socket">
        <xsl:call-template name="printGemSocket">
            <xsl:with-param name="color"><xsl:value-of select="@color" /></xsl:with-param>
            <xsl:with-param name="enchant"><xsl:value-of select="@enchant" /></xsl:with-param>
            <xsl:with-param name="icon"><xsl:value-of select="@icon" /></xsl:with-param>
        </xsl:call-template>
    </xsl:for-each>
    <xsl:if test="socketMatchEnchant">
        <br /><span><xsl:attribute name="class">
                <xsl:choose>
                    <xsl:when test="$numGemsMatched = count(socket)">bonusGreen</xsl:when>
                    <xsl:otherwise>setItemGray</xsl:otherwise>
                </xsl:choose>
            </xsl:attribute><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.socket-bonus']"/>&#160;<xsl:value-of select="socketMatchEnchant" />
	    </span>
    </xsl:if>
</xsl:template>

<xsl:template name="printGemSocket">
    <xsl:param name="color" />
    <xsl:param name="enchant" />
    <xsl:param name="icon" />
    <xsl:choose>
        <xsl:when test="string-length($enchant) &gt; 0">
            <br /><xsl:if test="string-length($icon) &gt; 0"><img src="{concat('images/icons/21x21/',$icon,'.png')}" class="socketImg p"/></xsl:if><xsl:value-of select="$enchant" />
        </xsl:when>
        <xsl:otherwise>
            <xsl:choose>
                <xsl:when test="$color = 'Meta'"><br /><span class="setItemGray"><img src="images/icons/Socket_Meta.png" class="socketImg"/><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.meta-socket']"/></span></xsl:when>
                <xsl:when test="$color = 'Red'"><br /><span class="setItemGray"><img src="images/icons/Socket_Red.png" class="socketImg"/><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.red-socket']"/></span></xsl:when>
                <xsl:when test="$color = 'Yellow'"><br /><span class="setItemGray"><img src="images/icons/Socket_Yellow.png" class="socketImg"/><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.yellow-socket']"/></span></xsl:when>
                <xsl:when test="$color = 'Blue'"><br /><span class="setItemGray"><img src="images/icons/Socket_Blue.png" class="socketImg"/><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.blue-socket']"/></span></xsl:when>
            </xsl:choose>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="randomEnchantData">
    <xsl:choose>
        <xsl:when test="suffix"><xsl:for-each select="enchant"><br /><xsl:value-of select="current()" /></xsl:for-each>
        </xsl:when>
        <xsl:otherwise><br /><span class="bonusGreen">&lt;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.random-enchant']"/>&gt;</span>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<!-- gem properties -->
<xsl:template match="gemProperties"><br /><xsl:value-of select="current()" /></xsl:template>

<!-- durability -->
<xsl:template match="durability">
    <br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.durability']"/>:&#160;<xsl:value-of select="@current" /> / <xsl:value-of select="@max" />
</xsl:template>

<!-- allowable races -->
<xsl:template match="allowableRaces"><br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.races']"/>: <xsl:for-each select="race"><xsl:if test="position() &gt; 1">, </xsl:if><xsl:value-of select="current()" /></xsl:for-each>
</xsl:template>

<!-- allowable classes -->
<xsl:template match="allowableClasses"><br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.classes']"/>: <xsl:for-each select="class"><xsl:if test="position() &gt; 1">, </xsl:if><xsl:value-of select="current()" /></xsl:for-each>
</xsl:template>

<!-- required level -->
<xsl:template match="requiredLevel"><xsl:if test="current() &gt; 1"><br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.requires-level']"/>&#160;<xsl:value-of select="current()" /></xsl:if>
</xsl:template>

<!-- minimum skill required -->
<xsl:template match="requiredSkill"><br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.requires']"/>&#160;<xsl:value-of select="@name" /> (<xsl:value-of select="@rank" />)</xsl:template>

<!-- ability required -->
<xsl:template match="requiredAbility"><br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.requires']"/>&#160;<xsl:value-of select="current()" /></xsl:template>

<!-- pvp rank required -->

<!-- pvp medal required -->

<!-- reputation required -->
<xsl:template match="requiredFaction"><br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.requires']"/>&#160;<xsl:value-of select="@name" /> - <xsl:call-template name="printFactionStanding">
    <xsl:with-param name="standing" select="@rep" /></xsl:call-template>
</xsl:template>

<xsl:template name="printFactionStanding">
    <xsl:param name="standing" />
    <xsl:choose>
        <xsl:when test="$standing = 0"><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.hated']"/></xsl:when>
        <xsl:when test="$standing = 1"><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.hostile']"/></xsl:when>
        <xsl:when test="$standing = 2"><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.unfriendly']"/></xsl:when>
        <xsl:when test="$standing = 3"><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.neutral']"/></xsl:when>
        <xsl:when test="$standing = 4"><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.friendly']"/></xsl:when>
        <xsl:when test="$standing = 5"><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.honored']"/></xsl:when>
        <xsl:when test="$standing = 6"><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.revered']"/></xsl:when>
        <xsl:when test="$standing = 7"><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.exalted']"/></xsl:when>
    </xsl:choose>
</xsl:template>

<!-- rating stats -->
<xsl:template match="bonusDefenseSkillRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.increase-defense']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusDodgeRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.increase-dodge']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusParryRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusParryRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusBlockRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusBlockRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusHitMeleeRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusHitMeleeRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusHitRangedRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusHitRangedRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusHitSpellRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.improve-spell']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusCritMeleeRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusCritMeleeRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusCritRangedRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusCritRangedRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusCritSpellRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.improve-spell-crit']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusHitTakenMeleeRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusHitTakenMeleeRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusHitTakenRangedRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusHitTakenRangedRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusHitTakenSpellRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusHitTakenSpellRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusCritTakenMeleeRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusCritTakenMeleeRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusCritTakenRangedRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusCritTakenRangedRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusCritTakenSpellRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusCritTakenSpellRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusHasteMeleeRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusHasteMeleeRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusHasteRangedRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusHasteRangedRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusHasteSpellRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusHasteSpellRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusHitRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.improve-hit-rating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusCritRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.improve-crit-strike']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusHitTakenRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusHitTakenRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusCritTakenRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusCritTakenRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusResilienceRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.improve-resilience']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>
<xsl:template match="bonusHasteRating">
    <br /><span class='bonusGreen'><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.bonusHasteRating']"/>&#160;<xsl:value-of select="current()" />.</span>
</xsl:template>

<!-- spell effect & charges -->
<xsl:template match="spellData">
    <xsl:for-each select="spell"><br />
        <xsl:choose>
            <xsl:when test="itemTooltip"><xsl:call-template name="printSpellTrigger">
                <xsl:with-param name="trigger" select="trigger" /></xsl:call-template>: <xsl:value-of select="desc" /><br />
                <xsl:if test="charges &gt; 1"><xsl:value-of select="charges" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.charges']"/><br /></xsl:if><br /><xsl:apply-templates select="itemTooltip" mode="recurse" /><br />
                <xsl:for-each select="reagent">
                    <xsl:choose>
                        <xsl:when test="position() = 1"><br /><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.requires']"/>&#160;</xsl:when><xsl:otherwise>, </xsl:otherwise>
                    </xsl:choose><xsl:value-of select="@name" /><xsl:if test="@count &gt; 1"> (<xsl:value-of select="@count" />)</xsl:if>
                </xsl:for-each>
            </xsl:when>
            <xsl:otherwise>
                <span class='bonusGreen'><xsl:call-template name="printSpellTrigger">
                <xsl:with-param name="trigger" select="trigger" /></xsl:call-template>: <xsl:value-of select="desc" /><xsl:if test="charges &gt; 1"><br /><xsl:value-of select="charges" />&#160;<xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.charges']"/></xsl:if>
                </span>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:for-each>
</xsl:template>

<xsl:template name="printSpellTrigger">
    <xsl:param name="trigger" />
    <xsl:choose>
        <xsl:when test="$trigger = 0"><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.use']"/></xsl:when>
        <xsl:when test="$trigger = 1"><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.equip']"/></xsl:when>
        <xsl:when test="$trigger = 2"><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.chance-on-hit']"/></xsl:when>
    </xsl:choose>
</xsl:template>

<!-- set description -->
<xsl:template match="setData">
    <xsl:variable name="numSetPieces" select="count(item/@equipped)" />
    <br /><br /><span class='setNameYellow'><xsl:value-of select="name" /> (<xsl:value-of select="$numSetPieces"/>/<xsl:value-of select="count(item)" />)</span>
    <xsl:apply-templates select="requiredSkill" />
    <xsl:for-each select="item">
        <br />
        <span style="margin-left:9px;"><xsl:choose>
                <xsl:when test="@equipped">
                    <xsl:attribute name="class">setItemYellow</xsl:attribute>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="class">setItemGray</xsl:attribute>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:value-of select="@name" />
        </span>
    </xsl:for-each>
    <br />
    <xsl:for-each select="setBonus">
        <br /><span><xsl:choose>
                <xsl:when test="$numSetPieces &gt;= @threshold"><xsl:attribute name="class">bonusGreen</xsl:attribute></xsl:when>
                <xsl:otherwise><xsl:attribute name="class">setItemGray</xsl:attribute>(<xsl:value-of select="@threshold" />) </xsl:otherwise>
            </xsl:choose><xsl:value-of select="$loc/strs/str[@id='armory.item-tooltip.set']"/>: <xsl:value-of select="@desc" />
        </span>
    </xsl:for-each>
</xsl:template>

<!-- item description text -->
<xsl:template match="desc">
    <br /><span class='myYellow'>"<xsl:value-of select="current()" />"</span>
</xsl:template>



</xsl:stylesheet>
