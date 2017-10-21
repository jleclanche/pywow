## Battlenet::Client::Authentication::LogonResponse3
channel=0x0, opcode=0x0 (S=>C):

  - `user` LogonResponse
    - `struct` Battlenet::Client::Authentication::LogonResponse
      - `user` Logon
        - `struct` Battlenet::Client::Authentication::Logon
      - `user` m_result
        - `choice` Battlenet::Client::Authentication::LogonResponse::Result
          [0x0,0x1]: range=0x2
  - `optional` m_raf
    - `user`
      - `blob` Battlenet::GameAccount::RafDataBlob
        [0x0,0x3e8]: range=0x3e9

## Battlenet::Client::Authentication::ResumeRequest
channel=0x0, opcode=0x1 (C=>S):

  - `user` RequestCommon
    - `struct` Battlenet::Client::Authentication::RequestCommon
      - `user` m_program
        - `fourcc` Battlenet::Program::Id
      - `user` m_platform
        - `fourcc` Battlenet::Platform::Id
      - `user` m_locale
        - `fourcc` Battlenet::Locale::Id
      - `user` m_versions
        - `array` Battlenet::Version::Records
          [0x0,0x3f]: range=0x40
          - `user`
            - `struct` Battlenet::Version::Record
              - `user` m_programId
                - `fourcc` Battlenet::Program::Id
              - `user` m_component
                - `fourcc` Battlenet::Version::Component
              - `user` m_version
                - `user` Battlenet::Version::Number
                  - `int` Battlenet::u32
                    [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_account
    - `asciistring` Battlenet::Account::Mail
      [0x3,0x140]: range=0x13e
  - `user` m_gameAccountRegion
    - `user` Battlenet::Region
      - `int` Battlenet::u8
        [0x0,0xff]: range=0x100, bytes=0x1
  - `user` m_gameAccountName
    - `asciistring` Battlenet::GameAccount::Name
      [0x1,0x20]: range=0x20

## Battlenet::Client::Authentication::ResumeResponse
channel=0x0, opcode=0x1 (S=>C):

  - `user` Resume
    - `struct` Battlenet::Client::Authentication::Resume
  - `user` m_result
    - `choice` Battlenet::Client::Authentication::ResumeResponse::Result
      [0x0,0x1]: range=0x2

## Battlenet::Client::Authentication::ProofRequest
channel=0x0, opcode=0x2 (S=>C):

  - `user` Proof
    - `struct` Battlenet::Client::Authentication::Proof
  - `user` m_request
    - `array` Battlenet::Authentication::ModuleRequest
      [0x0,0x4]: range=0x5
      - `user`
        - `struct` Battlenet::Authentication::ModuleInput
          - `user` m_id
            - `user` Battlenet::Authentication::ModuleId
              - `blob` Battlenet::Cache::Handle
                [0x1,0x1]: range=0x1
          - `user` m_data
            - `blob` Battlenet::Authentication::ModuleData
              [0x0,0x3ff]: range=0x400

## Battlenet::Client::Authentication::ProofResponse
channel=0x0, opcode=0x2 (C=>S):

  - `user` Proof
    - `struct` Battlenet::Client::Authentication::Proof
  - `user` m_response
    - `array` Battlenet::Authentication::ModuleResponse
      [0x0,0x4]: range=0x5
      - `user`
        - `struct` Battlenet::Authentication::ModuleOutput
          - `user` m_data
            - `blob` Battlenet::Authentication::ModuleData
              [0x0,0x3ff]: range=0x400

## Battlenet::Client::Authentication::Patch
channel=0x0, opcode=0x3 (S=>C):

  - `user` m_patch
    - `struct` Battlenet::Version::Patch
      - `user` m_programId
        - `fourcc` Battlenet::Program::Id
      - `user` m_component
        - `fourcc` Battlenet::Version::Component
      - `user` m_instructions
        - `asciistring` Battlenet::Version::Instructions
          [0x0,0xff]: range=0x100
  - `bool` m_more

## Battlenet::Client::Authentication::AuthorizedLicenses
channel=0x0, opcode=0x4 (S=>C):

  - `bool` m_persistent
  - `user` m_licenses
    - `array` Battlenet::License::InfoList
      [0x0,0x100]: range=0x101
      - `user`
        - `struct` Battlenet::License::Info
          - `user` m_id
            - `user` Battlenet::License::Id
              - `int` Battlenet::u32
                [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
          - `optional` m_expiration
            - `user`
              - `user` Battlenet::Time::Seconds
                - `int` Battlenet::s32
                  [-0x80000000L,0x7fffffff]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Authentication::GenerateSingleSignOnTokenRequest2
channel=0x0, opcode=0x8 (C=>S):

  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `optional` m_targetProgram
    - `user`
      - `fourcc` Battlenet::Program::Id

## Battlenet::Client::Authentication::GenerateSingleSignOnTokenResponse2
channel=0x0, opcode=0x8 (S=>C):

  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_result
    - `choice` Battlenet::Client::Authentication::GenerateSingleSignOnTokenResponse2::Result
      [0x0,0x1]: range=0x2

## Battlenet::Client::Authentication::LogonRequest3
channel=0x0, opcode=0x9 (C=>S):

  - `user` m_requestCommon
    - `struct` Battlenet::Client::Authentication::RequestCommon
      - `user` m_program
        - `fourcc` Battlenet::Program::Id
      - `user` m_platform
        - `fourcc` Battlenet::Platform::Id
      - `user` m_locale
        - `fourcc` Battlenet::Locale::Id
      - `user` m_versions
        - `array` Battlenet::Version::Records
          [0x0,0x3f]: range=0x40
          - `user`
            - `struct` Battlenet::Version::Record
              - `user` m_programId
                - `fourcc` Battlenet::Program::Id
              - `user` m_component
                - `fourcc` Battlenet::Version::Component
              - `user` m_version
                - `user` Battlenet::Version::Number
                  - `int` Battlenet::u32
                    [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `optional` m_account
    - `user`
      - `asciistring` Battlenet::Account::Mail
        [0x3,0x140]: range=0x13e
  - `user` m_compatibility
    - `int` Battlenet::u64
      [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8

## Battlenet::Client::Authentication::SingleSignOnRequest3
channel=0x0, opcode=0xa (C=>S):

  - `user` m_requestCommon
    - `struct` Battlenet::Client::Authentication::RequestCommon
      - `user` m_program
        - `fourcc` Battlenet::Program::Id
      - `user` m_platform
        - `fourcc` Battlenet::Platform::Id
      - `user` m_locale
        - `fourcc` Battlenet::Locale::Id
      - `user` m_versions
        - `array` Battlenet::Version::Records
          [0x0,0x3f]: range=0x40
          - `user`
            - `struct` Battlenet::Version::Record
              - `user` m_programId
                - `fourcc` Battlenet::Program::Id
              - `user` m_component
                - `fourcc` Battlenet::Version::Component
              - `user` m_version
                - `user` Battlenet::Version::Number
                  - `int` Battlenet::u32
                    [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_ssoId
    - `blob` Battlenet::Authentication::SingleSignOnId
      [0x0,0x200]: range=0x201
  - `user` m_compatibility
    - `int` Battlenet::u64
      [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8

## Battlenet::Client::Connection::Nul
channel=0x1, opcode=0x0 (S<=>C):


## Battlenet::Client::Connection::Boom
channel=0x1, opcode=0x1 (S=>C):

  - `user` m_error
    - `user` Battlenet::Error::Code
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2

## Battlenet::Client::Connection::RegulatorUpdate
channel=0x1, opcode=0x2 (S=>C):

  - `user` m_info
    - `choice` Battlenet::Regulator::Info
      [0x0,0x1]: range=0x2

## Battlenet::Client::Connection::ServerVersion
channel=0x1, opcode=0x3 (S=>C):

  - `user` m_version
    - `user` Battlenet::Server::Version
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Connection::STUNServers
channel=0x1, opcode=0x4 (S=>C):

  - `user` m_server1
    - `user` Battlenet::Client::AddressPort
      - `struct` Battlenet::IP4::AddressPort
        - `user` m_address
          - `blob` Battlenet::IP4::Address
            [0x84,0x1]: range=-0x82
        - `user` m_port
          - `blob` Battlenet::IP4::Port
            [0xf,0x3]: range=-0xb
  - `user` m_server2
    - `user` Battlenet::Client::AddressPort
      - `struct` Battlenet::IP4::AddressPort
        - `user` m_address
          - `blob` Battlenet::IP4::Address
            [0x84,0x1]: range=-0x82
        - `user` m_port
          - `blob` Battlenet::IP4::Port
            [0xf,0x3]: range=-0xb

## Battlenet::Client::Connection::EnableEncryption
channel=0x1, opcode=0x5 (C=>S):


## Battlenet::Client::Connection::LogoutRequest
channel=0x1, opcode=0x6 (C=>S):


## Battlenet::Client::Connection::DisconnectRequest
channel=0x1, opcode=0x7 (C=>S):

  - `user` m_error
    - `user` Battlenet::Error::Code
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2
  - `user` m_timeout
    - `user` Battlenet::Time::Tick
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Connection::ConnectionClosing
channel=0x1, opcode=0x9 (C=>S):

  - `optional` m_header
    - `user`
      - `struct` Battlenet::Header
        - `user` m_command
          - `int` Battlenet::Command
            [0x0,0x3f]: range=0x40, bytes=0x1
        - `optional` m_channel
          - `user`
            - `int` Battlenet::Channel
              [0x0,0xf]: range=0x10, bytes=0x1
  - `user` m_closingReason
    - `enum` Battlenet::Client::Connection::ClosingReason::Enum
      [0x1,0xd]: range=0xd
  - `user` m_badData
    - `blob` Battlenet::Client::Connection::PacketData
      [0x0,0x80]: range=0x81
  - `user` m_packets
    - `array` Battlenet::PacketInfoList
      [0x0,0x28]: range=0x29
      - `user`
        - `struct` Battlenet::PacketInfo
          - `user` m_layer
            - `fourcc` Battlenet::LayerId
          - `user` m_command
            - `fourcc` Battlenet::CommandName
          - `user` m_offset
            - `int` Battlenet::u16
              [0x0,0xffff]: range=0x10000, bytes=0x2
          - `user` m_size
            - `int` Battlenet::u16
              [0x0,0xffff]: range=0x10000, bytes=0x2
          - `user` m_time
            - `int` Battlenet::u32
              [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_now
    - `user` Battlenet::Time::Tick
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::WoWRealm::ListSubscribeRequest
channel=0x2, opcode=0x0 (C=>S):

  - `user` ListSubscribe
    - `struct` Battlenet::Client::WoWRealm::ListSubscribe

## Battlenet::Client::WoWRealm::ListSubscribeResponse
channel=0x2, opcode=0x0 (S=>C):

  - `user` ListSubscribe
    - `struct` Battlenet::Client::WoWRealm::ListSubscribe
  - `user` m_result
    - `choice` Battlenet::Client::WoWRealm::ListSubscribeResponse::Result
      [0x0,0x1]: range=0x2

## Battlenet::Client::WoWRealm::ListUnsubscribe
channel=0x2, opcode=0x1 (C=>S):


## Battlenet::Client::WoWRealm::ListUpdate
channel=0x2, opcode=0x2 (S=>C):

  - `user` m_id
    - `struct` Battlenet::WoW::RealmHandle
      - `user` m_region
        - `user` Battlenet::WoW::RegionId
          - `int` Battlenet::u8
            [0x0,0xff]: range=0x100, bytes=0x1
      - `user` m_site
        - `user` Battlenet::WoW::SiteId
          - `int` Battlenet::u8
            [0x0,0xff]: range=0x100, bytes=0x1
      - `user` m_realm
        - `user` Battlenet::Realm::Id
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_state
    - `choice` Battlenet::Client::WoWRealm::ListUpdate::State
      [0x0,0x1]: range=0x2

## Battlenet::Client::WoWRealm::ListComplete
channel=0x2, opcode=0x3 (S=>C):


## Battlenet::Client::WoWRealm::ToonReady
channel=0x2, opcode=0x6 (S=>C):

  - `user` m_name
    - `struct` Battlenet::Toon::FullName
      - `user` m_region
        - `user` Battlenet::Region
          - `int` Battlenet::u8
            [0x0,0xff]: range=0x100, bytes=0x1
      - `user` m_programId
        - `fourcc` Battlenet::Program::Id
      - `user` m_realm
        - `user` Battlenet::Realm::Id
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_name
        - `string` Battlenet::Toon::Name
          [0x2,0x19]: range=0x18
  - `user` m_handle
    - `struct` Battlenet::Toon::Handle
      - `user` m_region
        - `user` Battlenet::Region
          - `int` Battlenet::u8
            [0x0,0xff]: range=0x100, bytes=0x1
      - `user` m_programId
        - `fourcc` Battlenet::Program::Id
      - `user` m_realm
        - `user` Battlenet::Realm::Id
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_id
        - `user` Battlenet::Toon::Id
          - `int` Battlenet::u64
            [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8
  - `user` m_profileAddress
    - `struct` Battlenet::Profile::RecordAddress
      - `user` m_label
        - `user` Battlenet::Label
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_id
        - `user` Battlenet::Profile::RecordId
          - `int` Battlenet::u64
            [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8

## Battlenet::Client::WoWRealm::ToonLoggedOut
channel=0x2, opcode=0x7 (S=>C):


## Battlenet::Client::WoWRealm::JoinRequestV2
channel=0x2, opcode=0x8 (C=>S):

  - `user` JoinV2
    - `struct` Battlenet::Client::WoWRealm::JoinV2
  - `user` m_id
    - `struct` Battlenet::WoW::RealmHandle
      - `user` m_region
        - `user` Battlenet::WoW::RegionId
          - `int` Battlenet::u8
            [0x0,0xff]: range=0x100, bytes=0x1
      - `user` m_site
        - `user` Battlenet::WoW::SiteId
          - `int` Battlenet::u8
            [0x0,0xff]: range=0x100, bytes=0x1
      - `user` m_realm
        - `user` Battlenet::Realm::Id
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_clientSalt
    - `user` Battlenet::Client::WoWRealm::JoinSalt
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::WoWRealm::JoinResponseV2
channel=0x2, opcode=0x8 (S=>C):

  - `user` JoinV2
    - `struct` Battlenet::Client::WoWRealm::JoinV2
  - `user` m_result
    - `choice` Battlenet::Client::WoWRealm::JoinResponseV2::Result
      [0x0,0x1]: range=0x2

## Battlenet::Client::WoWRealm::MultiLogonRequestV2
channel=0x2, opcode=0x9 (C=>S):

  - `user` m_clientSalt
    - `user` Battlenet::Client::WoWRealm::JoinSalt
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Friends::FriendInvite
channel=0x3, opcode=0x1 (C=>S):

  - `user` FriendInviteBase
    - `struct` Battlenet::Client::Friends::FriendInviteBase
  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_target
    - `choice` Battlenet::Client::Defines::PlayerTarget
      [0x0,0x5]: range=0x6
  - `optional` m_msg
    - `user`
      - `string` Battlenet::Friends::Note
        [0x0,0x7f]: range=0x80
  - `bool` m_upgrade

## Battlenet::Client::Friends::FriendInviteNotify
channel=0x3, opcode=0x1 (S=>C):

  - `user` FriendInviteBase
    - `struct` Battlenet::Client::Friends::FriendInviteBase
  - `user` m_invite
    - `struct` Battlenet::Client::Friends::AccountInvite
      - `user` m_accountId
        - `user` Battlenet::Account::Id
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_update
        - `choice` Battlenet::Client::Friends::AccountInvite::Update
          [0x0,0x1]: range=0x2
  - `optional` m_isEndOfList
    - `bool`

## Battlenet::Client::Friends::FriendInviteResponse
channel=0x3, opcode=0x2 (C=>S):

  - `user` m_accountId
    - `user` Battlenet::Account::Id
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_response
    - `choice` Battlenet::Client::Friends::FriendInviteResponse::Response
      [0x0,0x1]: range=0x2

## Battlenet::Client::Friends::FriendInviteResult
channel=0x3, opcode=0x3 (S=>C):

  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_reason
    - `user` Battlenet::Error::Code
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2
  - `optional` m_accountFullName
    - `user`
      - `struct` Battlenet::Account::FullName
        - `user` m_givenName
          - `string` Battlenet::Account::NamePart
            [0x0,0x20]: range=0x21
        - `user` m_surname
          - `string` Battlenet::Account::NamePart
            [0x0,0x20]: range=0x21
  - `optional` m_toonFullName
    - `user`
      - `struct` Battlenet::Toon::FullName
        - `user` m_region
          - `user` Battlenet::Region
            - `int` Battlenet::u8
              [0x0,0xff]: range=0x100, bytes=0x1
        - `user` m_programId
          - `fourcc` Battlenet::Program::Id
        - `user` m_realm
          - `user` Battlenet::Realm::Id
            - `int` Battlenet::u32
              [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
        - `user` m_name
          - `string` Battlenet::Toon::Name
            [0x2,0x19]: range=0x18

## Battlenet::Client::Friends::FriendRemove
channel=0x3, opcode=0x4 (C=>S):

  - `user` m_id
    - `choice` Battlenet::Friends::PriorFriendId
      [0x0,0x1]: range=0x2

## Battlenet::Client::Friends::FriendNote
channel=0x3, opcode=0x5 (C=>S):

  - `user` m_target
    - `choice` Battlenet::Client::Defines::PlayerTarget
      [0x0,0x5]: range=0x6
  - `user` m_note
    - `string` Battlenet::Friends::Note
      [0x0,0x7f]: range=0x80

## Battlenet::Client::Friends::ToonsOfFriendsRequest
channel=0x3, opcode=0x6 (C=>S):

  - `user` ToonsOfFriendPacket
    - `struct` Battlenet::Client::Friends::ToonsOfFriendPacket
  - `user` m_accountId
    - `user` Battlenet::Account::Id
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Friends::ToonsOfFriendsNotify
channel=0x3, opcode=0x6 (S=>C):

  - `user` ToonsOfFriendPacket
    - `struct` Battlenet::Client::Friends::ToonsOfFriendPacket
  - `array` m_toons
    [0x0,0x64]: range=0x65
    - `user`
      - `struct` Battlenet::Friends::ToonOfFriend
        - `user` m_friendAccountId
          - `user` Battlenet::Account::Id
            - `int` Battlenet::u32
              [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
        - `user` m_toon
          - `struct` Battlenet::Toon::FullName
            - `user` m_region
              - `user` Battlenet::Region
                - `int` Battlenet::u8
                  [0x0,0xff]: range=0x100, bytes=0x1
            - `user` m_programId
              - `fourcc` Battlenet::Program::Id
            - `user` m_realm
              - `user` Battlenet::Realm::Id
                - `int` Battlenet::u32
                  [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
            - `user` m_name
              - `string` Battlenet::Toon::Name
                [0x2,0x19]: range=0x18
        - `user` m_profile
          - `struct` Battlenet::Profile::RecordAddress
            - `user` m_label
              - `user` Battlenet::Label
                - `int` Battlenet::u32
                  [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
            - `user` m_id
              - `user` Battlenet::Profile::RecordId
                - `int` Battlenet::u64
                  [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8
  - `bool` m_isEndOfList

## Battlenet::Client::Friends::BlockAdd
channel=0x3, opcode=0x8 (C=>S):

  - `user` m_target
    - `choice` Battlenet::Client::Defines::PlayerTarget
      [0x0,0x5]: range=0x6

## Battlenet::Client::Friends::BlockAddFailure
channel=0x3, opcode=0x9 (S=>C):

  - `user` m_reason
    - `user` Battlenet::Error::Code
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2

## Battlenet::Client::Friends::BlockRemove
channel=0x3, opcode=0xa (C=>S):

  - `user` m_target
    - `choice` Battlenet::Client::Defines::PlayerTarget
      [0x0,0x5]: range=0x6

## Battlenet::Client::Friends::GetFriendsOfFriend
channel=0x3, opcode=0xb (C=>S):

  - `user` m_accountId
    - `user` Battlenet::Account::Id
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Friends::MaxFriendsNotify
channel=0x3, opcode=0x15 (S=>C):

  - `user` m_maxFriends
    - `int` Battlenet::u16
      [0x0,0xffff]: range=0x10000, bytes=0x2
  - `user` m_maxInvites
    - `int` Battlenet::u16
      [0x0,0xffff]: range=0x10000, bytes=0x2

## Battlenet::Client::Friends::SendInvitationRequest
channel=0x3, opcode=0x1a (C=>S):

  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_target
    - `struct` Battlenet::Friends::FriendInvitationTarget
      - `optional` m_presenceId
        - `user`
          - `user` Battlenet::Presence::Id
            - `int` Battlenet::u32
              [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `optional` m_gameAccount
        - `user`
          - `struct` Battlenet::GameAccount::Handle
            - `user` m_region
              - `user` Battlenet::Region
                - `int` Battlenet::u8
                  [0x0,0xff]: range=0x100, bytes=0x1
            - `user` m_programId
              - `fourcc` Battlenet::Program::Id
            - `user` m_id
              - `user` Battlenet::GameAccount::Id
                - `int` Battlenet::u32
                  [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `optional` m_accountId
        - `user`
          - `user` Battlenet::Account::Id
            - `int` Battlenet::u32
              [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `optional` m_accountMail
        - `user`
          - `asciistring` Battlenet::Account::Mail
            [0x3,0x140]: range=0x13e
      - `optional` m_nickname
        - `user`
          - `string` Battlenet::Account::Nickname
            [0x0,0x1b]: range=0x1c
  - `user` m_params
    - `struct` Battlenet::Friends::FriendInvitationParams
      - `optional` m_invitationMsg
        - `user`
          - `string` Battlenet::Friends::Note
            [0x0,0x7f]: range=0x80
      - `fourcc` m_source
      - `user` m_role
        - `user` Battlenet::Friends::RoleId
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Friends::SendInvitationResult
channel=0x3, opcode=0x1b (S=>C):

  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_reason
    - `user` Battlenet::Error::Code
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2

## Battlenet::Client::Friends::FriendInvitationAddedNotify
channel=0x3, opcode=0x1c (S=>C):

  - `user` m_invitation
    - `struct` Battlenet::Friends::FriendInvitation
      - `optional` m_presenceId
        - `user`
          - `user` Battlenet::Presence::Id
            - `int` Battlenet::u32
              [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_accountId
        - `user` Battlenet::Account::Id
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `optional` m_fullName
        - `user`
          - `struct` Battlenet::Account::FullName
            - `user` m_givenName
              - `string` Battlenet::Account::NamePart
                [0x0,0x20]: range=0x21
            - `user` m_surname
              - `string` Battlenet::Account::NamePart
                [0x0,0x20]: range=0x21
      - `optional` m_nickname
        - `user`
          - `string` Battlenet::Account::Nickname
            [0x0,0x1b]: range=0x1c
      - `user` m_role
        - `user` Battlenet::Friends::RoleId
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `optional` m_msg
        - `user`
          - `string` Battlenet::Friends::Note
            [0x0,0x7f]: range=0x80
      - `user` m_createdTime
        - `user` Battlenet::Time::Seconds
          - `int` Battlenet::s32
            [-0x80000000L,0x7fffffff]: range=0x100000000L, bytes=0x4
      - `optional` m_profile
        - `user`
          - `struct` Battlenet::Profile::RecordAddress
            - `user` m_label
              - `user` Battlenet::Label
                - `int` Battlenet::u32
                  [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
            - `user` m_id
              - `user` Battlenet::Profile::RecordId
                - `int` Battlenet::u64
                  [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8
      - `optional` m_popupToast
        - `bool`
  - `optional` m_isEndOfList
    - `bool`

## Battlenet::Client::Friends::FriendInvitationRemovedNotify
channel=0x3, opcode=0x1d (S=>C):

  - `user` m_accountId
    - `user` Battlenet::Account::Id
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `optional` m_reason
    - `user`
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Friends::FriendsListNotify5
channel=0x3, opcode=0x1e (S=>C):

  - `array` m_friends
    [0x0,0x40]: range=0x41
    - `user`
      - `struct` Battlenet::Friends::FriendshipUpdate5
        - `user` m_update
          - `choice` Battlenet::Friends::FriendshipUpdate5::Update
            [0x0,0x1]: range=0x2
  - `optional` m_isEndOfList
    - `bool`

## Battlenet::Client::Friends::AccountBlockAddedNotify
channel=0x3, opcode=0x1f (S=>C):

  - `array` m_blocks
    [0x0,0x40]: range=0x41
    - `user`
      - `struct` Battlenet::Friends::AccountBlockContainer
        - `user` m_accountId
          - `user` Battlenet::Account::Id
            - `int` Battlenet::u32
              [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
        - `optional` m_fullName
          - `user`
            - `struct` Battlenet::Account::FullName
              - `user` m_givenName
                - `string` Battlenet::Account::NamePart
                  [0x0,0x20]: range=0x21
              - `user` m_surname
                - `string` Battlenet::Account::NamePart
                  [0x0,0x20]: range=0x21
        - `optional` m_nickname
          - `user`
            - `string` Battlenet::Account::Nickname
              [0x0,0x1b]: range=0x1c
        - `user` m_role
          - `user` Battlenet::Friends::RoleId
            - `int` Battlenet::u32
              [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `optional` m_isEndOfList
    - `bool`

## Battlenet::Client::Friends::AccountBlockRemovedNotify
channel=0x3, opcode=0x20 (S=>C):

  - `user` m_accountId
    - `user` Battlenet::Account::Id
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Friends::ToonBlockNotify
channel=0x3, opcode=0x21 (S=>C):

  - `array` m_blocks
    [0x0,0x40]: range=0x41
    - `user`
      - `struct` Battlenet::Friends::ToonBlockContainer
        - `user` m_toonName
          - `struct` Battlenet::Toon::FullName
            - `user` m_region
              - `user` Battlenet::Region
                - `int` Battlenet::u8
                  [0x0,0xff]: range=0x100, bytes=0x1
            - `user` m_programId
              - `fourcc` Battlenet::Program::Id
            - `user` m_realm
              - `user` Battlenet::Realm::Id
                - `int` Battlenet::u32
                  [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
            - `user` m_name
              - `string` Battlenet::Toon::Name
                [0x2,0x19]: range=0x18
        - `user` m_update
          - `choice` Battlenet::Friends::ToonBlockContainer::Update
            [0x0,0x1]: range=0x2
  - `optional` m_isEndOfList
    - `bool`

## Battlenet::Client::Friends::FriendsOfFriendResult
channel=0x3, opcode=0x22 (S=>C):

  - `user` m_result
    - `user` Battlenet::Error::Code
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2
  - `user` m_accountId
    - `user` Battlenet::Account::Id
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_friendAccounts
    - `array` Battlenet::Client::Friends::BasicFriendAccountsCompat2
      [0x0,0x64]: range=0x65
      - `user`
        - `struct` Battlenet::Friends::BasicFriendAccount2
          - `user` m_id
            - `user` Battlenet::Account::Id
              - `int` Battlenet::u32
                [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
          - `optional` m_fullName
            - `user`
              - `struct` Battlenet::Account::FullName
                - `user` m_givenName
                  - `string` Battlenet::Account::NamePart
                    [0x0,0x20]: range=0x21
                - `user` m_surname
                  - `string` Battlenet::Account::NamePart
                    [0x0,0x20]: range=0x21
          - `optional` m_nickname
            - `user`
              - `string` Battlenet::Account::Nickname
                [0x0,0x1b]: range=0x1c
          - `user` m_role
            - `user` Battlenet::Friends::RoleId
              - `int` Battlenet::u32
                [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `optional` m_isEndOfList
    - `bool`

## Battlenet::Presence::SharedPackets::UpdateNotify
channel=0x4, opcode=0x0 (S=>C):

  - `user` UpdateBase
    - `struct` Battlenet::Presence::SharedPackets::UpdateBase
  - `user` m_idLocal
    - `user` Battlenet::Presence::Id
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_idMaster
    - `user` Battlenet::Presence::Id
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_online
    - `user` Battlenet::Presence::Online
      - `int` Battlenet::u8
        [0x0,0xff]: range=0x100, bytes=0x1
  - `bool` m_serverOnly
  - `user` m_update
    - `struct` Battlenet::Presence::Update
      - `user` m_handlesCleared
        - `array` Battlenet::Presence::HandleList
          [0x0,0xf]: range=0x10
          - `user`
            - `user` Battlenet::Presence::Handle
              - `int` Battlenet::u32
                [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_handles
        - `array` Battlenet::Presence::HandleList
          [0x0,0xf]: range=0x10
          - `user`
            - `user` Battlenet::Presence::Handle
              - `int` Battlenet::u32
                [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `array` m_varSizes
        [0x0,0xf]: range=0x10
        - `user`
          - `user` Battlenet::Presence::TypeSize
            - `int` Battlenet::u16
              [0x0,0xffff]: range=0x10000, bytes=0x2
      - `blob` m_fieldData
        [0x0,0x400]: range=0x401
  - `optional` m_level0
    - `user`
      - `struct` Battlenet::Presence::SharedPackets::Level0Info
        - `user` m_target
          - `user` Battlenet::Presence::SubscriberId
            - `user` Battlenet::Presence::Id
              - `int` Battlenet::u32
                [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
        - `bool` m_isLastPacket

## Battlenet::Presence::SharedPackets::UpdateRequest
channel=0x4, opcode=0x0 (C=>S):

  - `user` UpdateBase
    - `struct` Battlenet::Presence::SharedPackets::UpdateBase
  - `user` m_id
    - `user` Battlenet::Presence::Id
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_handle
    - `user` Battlenet::Presence::Handle
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_value
    - `choice` Battlenet::Presence::FieldVal
      [0x0,0x1d]: range=0x1e

## Battlenet::Presence::SharedPackets::FieldSpecAnnounce
channel=0x4, opcode=0x1 (S=>C):

  - `user` m_list
    - `array` Battlenet::Presence::FieldSpecAnnounceList
      [0x0,0x64]: range=0x65
      - `user`
        - `struct` Battlenet::Presence::FieldSpecAnnounceEntry
          - `user` m_handle
            - `user` Battlenet::Presence::Handle
              - `int` Battlenet::u32
                [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
          - `user` m_spec
            - `struct` Battlenet::Presence::FieldSpec
              - `user` m_id
                - `enum` Battlenet::Presence::TypeEnum::Enum
                  [0x0,0xff]: range=0x100
              - `bool` m_writable
              - `bool` m_ephemeral
              - `bool` m_serverOnly
              - `bool` m_clientOnly
              - `user` m_size
                - `choice` Battlenet::Presence::FieldSpec::Size
                  [0x0,0x1]: range=0x2

## Battlenet::Client::Presence::StatisticsSubscribe
channel=0x4, opcode=0x2 (C=>S):

  - `bool` m_on

## Battlenet::Client::Presence::StatisticsUpdate
channel=0x4, opcode=0x3 (S=>C):

  - `user` m_statistics
    - `array` Battlenet::Statistics::ClientValues
      [0x0,0x3f]: range=0x40
      - `user`
        - `struct` Battlenet::Statistics::ClientValue
          - `user` m_report
            - `user` Battlenet::Statistics::ReportId
              - `int` Battlenet::u32
                [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
          - `user` m_value
            - `user` Battlenet::Statistics::Value
              - `int` Battlenet::u64
                [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8

## Battlenet::Client::Chat::JoinRequest2
channel=0x5, opcode=0x0 (C=>S):

  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_key
    - `choice` Battlenet::Conference::LocatorKey
      [0x0,0x3]: range=0x4

## Battlenet::Client::Chat::MembershipChangeNotify
channel=0x5, opcode=0x1 (S=>C):

  - `bool` m_endOfInitial
  - `user` m_channelIndex
    - `int` Battlenet::Chat::ClientChannelIndex
      [0x0,0x6]: range=0x7, bytes=0x1
  - `user` m_changes
    - `array` Battlenet::Chat::MembershipChangeList
      [0x1,0x40]: range=0x40
      - `user`
        - `choice` Battlenet::Chat::MembershipChange
          [0x0,0x2]: range=0x3

## Battlenet::Client::Chat::LeaveRequest
channel=0x5, opcode=0x2 (C=>S):

  - `user` m_channelIndex
    - `int` Battlenet::Chat::ClientChannelIndex
      [0x0,0x6]: range=0x7, bytes=0x1

## Battlenet::Client::Chat::InviteRequest
channel=0x5, opcode=0x3 (C=>S):

  - `user` m_channelIndex
    - `int` Battlenet::Chat::ClientChannelIndex
      [0x0,0x6]: range=0x7, bytes=0x1
  - `user` m_target
    - `choice` Battlenet::Client::Defines::PlayerTarget
      [0x0,0x5]: range=0x6
  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Chat::InviteNotify
channel=0x5, opcode=0x4 (S=>C):

  - `user` m_channelIndex
    - `int` Battlenet::Chat::ClientChannelIndex
      [0x0,0x6]: range=0x7, bytes=0x1
  - `user` m_inviterPresence
    - `user` Battlenet::Presence::Id
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_channelType
    - `enum` Battlenet::Chat::ChannelType2::Enum
      [0x0,0xf]: range=0x10

## Battlenet::Client::Chat::InviteCanceled
channel=0x5, opcode=0x7 (S=>C):

  - `user` m_channelIndex
    - `int` Battlenet::Chat::ClientChannelIndex
      [0x0,0x6]: range=0x7, bytes=0x1
  - `user` m_reason
    - `user` Battlenet::Error::Code
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2

## Battlenet::Client::Chat::CreateAndInviteRequest
channel=0x5, opcode=0xa (C=>S):

  - `user` m_createToken
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_inviteToken
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_channelType
    - `enum` Battlenet::Chat::ChannelType::Enum
      [0x0,0x3]: range=0x4
  - `user` m_target
    - `choice` Battlenet::Client::Defines::PlayerTarget
      [0x0,0x5]: range=0x6

## Battlenet::Client::Chat::MessageSend
channel=0x5, opcode=0xb (C=>S):

  - `user` Message
    - `struct` Battlenet::Client::Chat::Message
  - `user` m_channelIndex
    - `int` Battlenet::Chat::ClientChannelIndex
      [0x0,0x6]: range=0x7, bytes=0x1
  - `user` m_body
    - `string` Battlenet::Chat::Line
      [0x0,0xff]: range=0x100

## Battlenet::Client::Chat::MessageRecv
channel=0x5, opcode=0xb (S=>C):

  - `user` Message
    - `struct` Battlenet::Client::Chat::Message
  - `user` m_channelIndex
    - `int` Battlenet::Chat::ClientChannelIndex
      [0x0,0x6]: range=0x7, bytes=0x1
  - `user` m_memberHandle
    - `user` Battlenet::Chat::MemberHandle
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_body
    - `string` Battlenet::Chat::Line
      [0x0,0xff]: range=0x100

## Battlenet::Client::Chat::MessageUndeliverable
channel=0x5, opcode=0xc (S=>C):

  - `user` m_channelIndex
    - `int` Battlenet::Chat::ClientChannelIndex
      [0x0,0x6]: range=0x7, bytes=0x1
  - `user` m_reason
    - `user` Battlenet::Error::Code
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2

## Battlenet::Client::Chat::DatagramConnectionUpdate
channel=0x5, opcode=0xd (S<=>C):

  - `user` m_target
    - `choice` Battlenet::Client::Defines::PlayerTarget
      [0x0,0x5]: range=0x6
  - `user` m_info
    - `struct` Battlenet::Chat::DatagramConnectionInfo
      - `user` m_instance
        - `fourcc` Battlenet::DatagramConnection::InstanceCode
      - `user` m_natType
        - `enum` Battlenet::DatagramConnection::NATType::Enum
          [0x0,0x3]: range=0x4
      - `user` m_addressPort
        - `user` Battlenet::Client::AddressPort
          - `struct` Battlenet::IP4::AddressPort
            - `user` m_address
              - `blob` Battlenet::IP4::Address
                [0x84,0x1]: range=-0x82
            - `user` m_port
              - `blob` Battlenet::IP4::Port
                [0xf,0x3]: range=-0xb
      - `user` m_boundAddressPort
        - `user` Battlenet::Client::AddressPort
          - `struct` Battlenet::IP4::AddressPort
            - `user` m_address
              - `blob` Battlenet::IP4::Address
                [0x84,0x1]: range=-0x82
            - `user` m_port
              - `blob` Battlenet::IP4::Port
                [0xf,0x3]: range=-0xb
      - `user` m_arbitrationNotify
        - `enum` Battlenet::DatagramConnection::ArbitrationNotify::Enum
          [0x0,0x6]: range=0x7
      - `user` m_token
        - `user` Battlenet::DatagramConnection::ConnectionToken
          - `int` Battlenet::u8
            [0x0,0xff]: range=0x100, bytes=0x1
      - `user` m_connectAttemptToken
        - `user` Battlenet::DatagramConnection::ConnectAttemptToken
          - `int` Battlenet::u8
            [0x0,0xff]: range=0x100, bytes=0x1

## Battlenet::Client::Chat::ReportSpamRequest
channel=0x5, opcode=0xe (C=>S):

  - `user` m_target
    - `choice` Battlenet::Client::Defines::PlayerTarget
      [0x0,0x5]: range=0x6

## Battlenet::Client::Chat::InviteFailed
channel=0x5, opcode=0xf (S=>C):

  - `user` m_channelIndex
    - `int` Battlenet::Chat::ClientChannelIndex
      [0x0,0x6]: range=0x7, bytes=0x1
  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_reason
    - `user` Battlenet::Error::Code
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2

## Battlenet::Client::Chat::SystemMessage
channel=0x5, opcode=0x10 (S=>C):

  - `user` m_body
    - `struct` Battlenet::Chat::SystemMessage
      - `user` m_messageId
        - `user` Battlenet::Error::Code
          - `int` Battlenet::u16
            [0x0,0xffff]: range=0x10000, bytes=0x2
      - `optional` m_argument
        - `user`
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Chat::MessageBlocked
channel=0x5, opcode=0x12 (S=>C):

  - `user` m_channelIndex
    - `int` Battlenet::Chat::ClientChannelIndex
      [0x0,0x6]: range=0x7, bytes=0x1
  - `user` m_memberHandle
    - `user` Battlenet::Chat::MemberHandle
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Chat::WhisperSend
channel=0x5, opcode=0x13 (C=>S):

  - `user` Whisper
    - `struct` Battlenet::Client::Chat::Whisper
  - `user` m_target
    - `choice` Battlenet::Client::Defines::PlayerTarget
      [0x0,0x5]: range=0x6
  - `user` m_body
    - `string` Battlenet::Chat::Line
      [0x0,0xff]: range=0x100

## Battlenet::Client::Chat::WhisperRecv
channel=0x5, opcode=0x13 (S=>C):

  - `user` Whisper
    - `struct` Battlenet::Client::Chat::Whisper
  - `user` m_sender
    - `struct` Battlenet::Toon::FullName
      - `user` m_region
        - `user` Battlenet::Region
          - `int` Battlenet::u8
            [0x0,0xff]: range=0x100, bytes=0x1
      - `user` m_programId
        - `fourcc` Battlenet::Program::Id
      - `user` m_realm
        - `user` Battlenet::Realm::Id
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_name
        - `string` Battlenet::Toon::Name
          [0x2,0x19]: range=0x18
  - `user` m_body
    - `string` Battlenet::Chat::Line
      [0x0,0xff]: range=0x100

## Battlenet::Client::Chat::WhisperUndeliverable
channel=0x5, opcode=0x14 (S=>C):

  - `user` m_target
    - `choice` Battlenet::Client::Defines::PlayerTarget
      [0x0,0x5]: range=0x6
  - `user` m_reason
    - `user` Battlenet::Error::Code
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2

## Battlenet::Client::Chat::EnumCategoryDescriptions
channel=0x5, opcode=0x15 (C=>S):


## Battlenet::Client::Chat::CategoryDescriptions
channel=0x5, opcode=0x16 (S=>C):

  - `user` m_list
    - `array` Battlenet::Conference::CategoryDescriptionList
      [0x0,0x3f]: range=0x40
      - `user`
        - `struct` Battlenet::Conference::CategoryDescription
          - `user` m_id
            - `user` Battlenet::Conference::CategoryId
              - `int` Battlenet::u8
                [0x0,0xff]: range=0x100, bytes=0x1
          - `user` m_name
            - `user` Battlenet::Conference::ChannelNameStringId
              - `int` Battlenet::u16
                [0x0,0xffff]: range=0x10000, bytes=0x2
          - `user` m_sortOrder
            - `user` Battlenet::Conference::SortOrder
              - `user` Battlenet::Conference::IndexId
                - `int` Battlenet::u16
                  [0x0,0xffff]: range=0x10000, bytes=0x2
  - `bool` m_isLast

## Battlenet::Client::Chat::EnumConferenceDescriptions
channel=0x5, opcode=0x17 (C=>S):


## Battlenet::Client::Chat::ConferenceDescriptions
channel=0x5, opcode=0x18 (S=>C):

  - `user` m_list
    - `array` Battlenet::Conference::FullConferenceDescriptionList
      [0x0,0x3f]: range=0x40
      - `user`
        - `struct` Battlenet::Conference::FullConferenceDescription
          - `user` m_parentCategory
            - `user` Battlenet::Conference::CategoryId
              - `int` Battlenet::u8
                [0x0,0xff]: range=0x100, bytes=0x1
          - `user` m_name
            - `struct` Battlenet::Conference::ShardName
              - `user` m_key
                - `choice` Battlenet::Conference::LocatorKey
                  [0x0,0x3]: range=0x4
              - `user` m_index
                - `user` Battlenet::Conference::IndexId
                  - `int` Battlenet::u16
                    [0x0,0xffff]: range=0x10000, bytes=0x2
          - `user` m_sortOrder
            - `user` Battlenet::Conference::SortOrder
              - `user` Battlenet::Conference::IndexId
                - `int` Battlenet::u16
                  [0x0,0xffff]: range=0x10000, bytes=0x2
          - `user` m_configuration
            - `struct` Battlenet::Conference::ConferenceConfiguration
              - `U` m_maxMembers
              - `U` m_allowedPrograms
              - `U` m_allowedRealms
              - `U` m_flags
              - `nop` m_targetProportion
              - `U`
          - `user` m_id
            - `user` Battlenet::Conference::Id
              - `int` Battlenet::u32
                [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `bool` m_isLast

## Battlenet::Client::Chat::EnumConferenceMemberCounts
channel=0x5, opcode=0x19 (C=>S):


## Battlenet::Client::Chat::ConferenceMemberCounts
channel=0x5, opcode=0x1a (S=>C):

  - `user` m_list
    - `array` Battlenet::Conference::MembershipInfoList
      [0x0,0x3f]: range=0x40
      - `user`
        - `struct` Battlenet::Conference::MembershipInfo
          - `user` m_id
            - `user` Battlenet::Conference::Id
              - `int` Battlenet::u32
                [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
          - `user` m_numMembers
            - `user` Battlenet::Conference::MembershipCount
              - `int` Battlenet::u16
                [0x0,0xffff]: range=0x10000, bytes=0x2
          - `bool` m_isFull
  - `bool` m_isLast
  - `optional` m_time
    - `user`
      - `user` Battlenet::Time::Seconds
        - `int` Battlenet::s32
          [-0x80000000L,0x7fffffff]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Chat::JoinNotify2
channel=0x5, opcode=0x1b (S=>C):

  - `optional` m_token
    - `user`
      - `user` Battlenet::Token
        - `int` Battlenet::u32
          [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_result
    - `choice` Battlenet::Chat::JoinNotifyResult2
      [0x0,0x1]: range=0x2

## Battlenet::Client::Chat::ConfigChanged
channel=0x5, opcode=0x1d (S=>C):

  - `user` m_index
    - `int` Battlenet::Chat::ClientChannelIndex
      [0x0,0x6]: range=0x7, bytes=0x1
  - `user` m_config
    - `struct` Battlenet::Conference::ConferenceConfiguration
      - `U` m_maxMembers
      - `U` m_allowedPrograms
      - `U` m_allowedRealms
      - `U` m_flags
      - `nop` m_targetProportion
      - `U`

## Battlenet::Client::Chat::WhisperEchoRecv
channel=0x5, opcode=0x1e (S=>C):

  - `user` WhisperEcho
    - `struct` Battlenet::Client::Chat::WhisperEcho
  - `user` m_sender
    - `struct` Battlenet::Toon::FullName
      - `user` m_region
        - `user` Battlenet::Region
          - `int` Battlenet::u8
            [0x0,0xff]: range=0x100, bytes=0x1
      - `user` m_programId
        - `fourcc` Battlenet::Program::Id
      - `user` m_realm
        - `user` Battlenet::Realm::Id
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_name
        - `string` Battlenet::Toon::Name
          [0x2,0x19]: range=0x18
  - `user` m_body
    - `string` Battlenet::Chat::Line
      [0x0,0xff]: range=0x100

## Battlenet::Client::Chat::GetMemberCountRequest
channel=0x5, opcode=0x1f (C=>S):

  - `user` GetMemberCount
    - `struct` Battlenet::Client::Chat::GetMemberCount
  - `user` m_name
    - `string` Battlenet::Conference::PrivateName
      [0x0,0x1f]: range=0x20

## Battlenet::Client::Chat::GetMemberCountResponse
channel=0x5, opcode=0x1f (S=>C):

  - `user` GetMemberCount
    - `struct` Battlenet::Client::Chat::GetMemberCount
  - `user` m_name
    - `string` Battlenet::Conference::PrivateName
      [0x0,0x1f]: range=0x20
  - `user` m_count
    - `user` Battlenet::Conference::MembershipCount
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2

## Battlenet::Client::Chat::ModifyChannelListRequest2
channel=0x5, opcode=0x20 (C=>S):

  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_index
    - `int` Battlenet::u8
      [0x0,0xff]: range=0x100, bytes=0x1
  - `user` m_key
    - `choice` Battlenet::Conference::LocatorKey
      [0x0,0x3]: range=0x4
  - `user` m_type
    - `enum` Battlenet::Client::Chat::ChannelListType::Enum
      [0x0,0x1]: range=0x2

## Battlenet::Client::Chat::ModifyChannelListResponse2
channel=0x5, opcode=0x21 (S=>C):

  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_result
    - `choice` Battlenet::Client::Chat::ModifyChannelListResponse2::Result
      [0x0,0x1]: range=0x2

## Battlenet::Client::Chat::GameDataSendRequest
channel=0x5, opcode=0x22 (C=>S):

  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_target
    - `choice` Battlenet::Client::Defines::PlayerTarget
      [0x0,0x5]: range=0x6
  - `user` m_body
    - `string` Battlenet::Chat::GameData
      [0x0,0xfff]: range=0x1000

## Battlenet::Client::Chat::GameDataSendResponse
channel=0x5, opcode=0x23 (S=>C):

  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_result
    - `user` Battlenet::Error::Code
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2

## Battlenet::Client::Chat::GameDataRecv
channel=0x5, opcode=0x24 (S=>C):

  - `user` m_sender
    - `choice` Battlenet::Client::Defines::PlayerTarget
      [0x0,0x5]: range=0x6
  - `user` m_body
    - `string` Battlenet::Chat::GameData
      [0x0,0xfff]: range=0x1000

## Battlenet::Client::Support::ComplaintRequest2
channel=0x7, opcode=0x1 (C=>S):

  - `user` Complaint2
    - `struct` Battlenet::Client::Support::Complaint2
  - `user` m_info
    - `struct` Battlenet::Support::ComplaintInfo2
      - `user` m_code
        - `enum` Battlenet::Support::ComplaintCode::Enum
          [0x0,0xff]: range=0x100
      - `optional` m_note
        - `user`
          - `string` Battlenet::Support::ComplaintNote2
            [0x0,0x3ff]: range=0x400
      - `user` m_target
        - `choice` Battlenet::Support::ComplaintInfo2::Target
          [0x0,0x3]: range=0x4

## Battlenet::Client::Achievement::ListenRequest
channel=0x8, opcode=0x0 (C=>S):

  - `user` m_address
    - `struct` Battlenet::Profile::RecordAddress
      - `user` m_label
        - `user` Battlenet::Label
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_id
        - `user` Battlenet::Profile::RecordId
          - `int` Battlenet::u64
            [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8
  - `user` m_mode
    - `enum` Battlenet::Achievement::ListenMode::Enum
      [0x0,0xff]: range=0x100
  - `user` m_scope
    - `enum` Battlenet::Achievement::ListenScope::Enum
      [0x0,0xff]: range=0x100

## Battlenet::Client::Achievement::Data
channel=0x8, opcode=0x2 (S=>C):

  - `user` m_address
    - `struct` Battlenet::Profile::RecordAddress
      - `user` m_label
        - `user` Battlenet::Label
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_id
        - `user` Battlenet::Profile::RecordId
          - `int` Battlenet::u64
            [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8
  - `user` m_segment
    - `choice` Battlenet::Achievement::DataSegment
      [0x0,0x2]: range=0x3

## Battlenet::Client::Achievement::CriteriaFlushRequest
channel=0x8, opcode=0x3 (C=>S):

  - `user` CriteriaFlush
    - `struct` Battlenet::Client::Achievement::CriteriaFlush
  - `user` m_flushToken
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_address
    - `struct` Battlenet::Profile::RecordAddress
      - `user` m_label
        - `user` Battlenet::Label
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_id
        - `user` Battlenet::Profile::RecordId
          - `int` Battlenet::u64
            [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8
  - `array` m_deltas
    [0x0,0x40]: range=0x41
    - `user`
      - `struct` Battlenet::Achievement::CriteriaUpdateRecord
        - `user` m_criteriaId
          - `user` Battlenet::Achievement::CriteriaId
            - `int` Battlenet::u64
              [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8
        - `optional` m_startTime
          - `user`
            - `user` Battlenet::Time::Seconds
              - `int` Battlenet::s32
                [-0x80000000L,0x7fffffff]: range=0x100000000L, bytes=0x4
        - `optional` m_quantity
          - `user`
            - `user` Battlenet::Achievement::CriteriaQuantity
              - `int` Battlenet::u64
                [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8
        - `user` m_flags
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Achievement::CriteriaFlushResponse
channel=0x8, opcode=0x3 (S=>C):

  - `user` CriteriaFlush
    - `struct` Battlenet::Client::Achievement::CriteriaFlush
  - `user` m_flushToken
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_code
    - `user` Battlenet::Error::Code
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2

## Battlenet::Client::Achievement::AchievementHandleUpdate
channel=0x8, opcode=0x4 (S=>C):

  - `user` m_info
    - `struct` Battlenet::Achievement::ProgramHandleAggregation
      - `user` m_program
        - `fourcc` Battlenet::Program::Id
      - `user` m_handle
        - `blob` Battlenet::Cache::Handle
          [0x1,0x1]: range=0x1

## Battlenet::Client::Achievement::ChangeTrophyCaseResult
channel=0x8, opcode=0x6 (S=>C):

  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_result
    - `user` Battlenet::Error::Code
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2

## Battlenet::Client::Cache::GatewayLookupRequest
channel=0xb, opcode=0x2 (C=>S):

  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_purposeCode
    - `fourcc` Battlenet::Cache::Usage
  - `user` m_cacheHandle
    - `blob` Battlenet::Cache::Handle
      [0x1,0x1]: range=0x1
  - `user` m_challenge
    - `user` Battlenet::Authentication::SecondarySalt
      - `blob` Battlenet::Session::Salt
        [0x84,0x1]: range=-0x82

## Battlenet::Client::Cache::GatewayLookupResponse
channel=0xb, opcode=0x3 (S=>C):

  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_result
    - `choice` Battlenet::Client::Cache::GatewayLookupResponse::Result
      [0x0,0x1]: range=0x2

## Battlenet::Client::Cache::ConnectRequest
channel=0xb, opcode=0x4 (C=>S):

  - `user` Connect
    - `struct` Battlenet::Client::Cache::Connect
  - `user` m_saveId
    - `user` Battlenet::Cache::SaveId
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_authProof
    - `blob` Battlenet::Authentication::SecondaryProof
      [0x4,0x3]: range=0x0
  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_version
    - `struct` Battlenet::Version::Record
      - `user` m_programId
        - `fourcc` Battlenet::Program::Id
      - `user` m_component
        - `fourcc` Battlenet::Version::Component
      - `user` m_version
        - `user` Battlenet::Version::Number
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Cache::ConnectResponse
channel=0xb, opcode=0x4 (S=>C):

  - `user` Connect
    - `struct` Battlenet::Client::Cache::Connect
  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_authProof
    - `blob` Battlenet::Authentication::SecondaryProof
      [0x4,0x3]: range=0x0

## Battlenet::Client::Cache::PublishListResponse
channel=0xb, opcode=0x7 (S=>C):

  - `user` PublishList
    - `struct` Battlenet::Client::Cache::PublishList
  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_result
    - `choice` Battlenet::Client::Cache::PublishListResponse::Result
      [0x0,0x1]: range=0x2

## Battlenet::Client::Cache::DataChunk
channel=0xb, opcode=0x7 (C=>S):

  - `user` m_data
    - `blob` Battlenet::Cache::CacheBlob
      [0x0,0x400]: range=0x401

## Battlenet::Client::Cache::Result
channel=0xb, opcode=0x8 (S=>C):

  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_result
    - `choice` Battlenet::Cache::Shared::Result
      [0x0,0x3]: range=0x4

## Battlenet::Client::Cache::GetStreamItemsRequest
channel=0xb, opcode=0x9 (C=>S):

  - `user` GetStreamItems
    - `struct` Battlenet::Client::Cache::GetStreamItems
  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `int` m_maxItems
    [0x1,0x32]: range=0x32, bytes=0x1
  - `user` m_referenceTime
    - `user` Battlenet::Time::Seconds
      - `int` Battlenet::s32
        [-0x80000000L,0x7fffffff]: range=0x100000000L, bytes=0x4
  - `user` m_direction
    - `enum` Battlenet::Cache::StreamDirection::Enum
      [0x0,0x1]: range=0x2
  - `user` m_stream
    - `choice` Battlenet::Cache::StreamId
      [0x0,0x1]: range=0x2
  - `user` m_locale
    - `fourcc` Battlenet::Locale::Id

## Battlenet::Client::Cache::GetStreamItemsResponse
channel=0xb, opcode=0x9 (S=>C):

  - `user` GetStreamItems
    - `struct` Battlenet::Client::Cache::GetStreamItems
  - `user` m_items
    - `array` Battlenet::Client::Cache::StreamItemList
      [0x0,0x31]: range=0x32
      - `user`
        - `struct` Battlenet::Cache::StreamItem
          - `user` m_publicationTime
            - `user` Battlenet::Time::Seconds
              - `int` Battlenet::s32
                [-0x80000000L,0x7fffffff]: range=0x100000000L, bytes=0x4
          - `user` m_contentHandle
            - `blob` Battlenet::Cache::Handle
              [0x1,0x1]: range=0x1
  - `user` m_offset
    - `int` Battlenet::u16
      [0x0,0xffff]: range=0x10000, bytes=0x2
  - `user` m_totalNumItems
    - `int` Battlenet::u16
      [0x0,0xffff]: range=0x10000, bytes=0x2
  - `user` m_token
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4

## Battlenet::Client::Cache::GetConfigHandleResponse
channel=0xb, opcode=0xa (S=>C):

  - `user` GetConfigHandle
    - `struct` Battlenet::Client::Cache::GetConfigHandle
  - `user` RPC::Response
    - `struct` Battlenet::RPC::Response
      - `user` m_correlationId
        - `int` Battlenet::u32
          [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_result
    - `choice` Battlenet::Client::Cache::GetConfigHandleResponse::Result
      [0x0,0x1]: range=0x2

## Battlenet::Client::Profile::ReadRequest
channel=0xe, opcode=0x0 (C=>S):

  - `user` Read
    - `struct` Battlenet::Client::Profile::Read
  - `user` m_requestId
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_recordAddress
    - `struct` Battlenet::Profile::RecordAddress
      - `user` m_label
        - `user` Battlenet::Label
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_id
        - `user` Battlenet::Profile::RecordId
          - `int` Battlenet::u64
            [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8
  - `user` m_specification
    - `struct` Battlenet::Profile::FullReadSpecification
      - `user` m_selection
        - `choice` Battlenet::Profile::ReadSelection
          [0x0,0x4]: range=0x5
      - `optional` m_reader
        - `user`
          - `array` Battlenet::Profile::ReaderList
            [0x0,0x8]: range=0x9
            - `user`
              - `user` Battlenet::Profile::EntityId
                - `user` Battlenet::Profile::RecordId
                  - `int` Battlenet::u64
                    [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8

## Battlenet::Client::Profile::ReadResponse
channel=0xe, opcode=0x0 (S=>C):

  - `user` Read
    - `struct` Battlenet::Client::Profile::Read
  - `user` m_requestId
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_result
    - `choice` Battlenet::Profile::ProfileDataResponse
      [0x0,0x2]: range=0x3

## Battlenet::Client::Profile::AddressQueryRequest
channel=0xe, opcode=0x1 (C=>S):

  - `user` AddressQuery
    - `struct` Battlenet::Client::Profile::AddressQuery
  - `user` m_requestId
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_playerTarget
    - `choice` Battlenet::Client::Defines::PlayerTarget
      [0x0,0x5]: range=0x6

## Battlenet::Client::Profile::AddressQueryResponse
channel=0xe, opcode=0x1 (S=>C):

  - `user` AddressQuery
    - `struct` Battlenet::Client::Profile::AddressQuery
  - `user` m_requestId
    - `user` Battlenet::Token
      - `int` Battlenet::u32
        [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
  - `user` m_result
    - `choice` Battlenet::Client::Profile::AddressQueryResponse::Result
      [0x0,0x1]: range=0x2

## Battlenet::Client::Profile::ResolveToonHandleToNameRequest
channel=0xe, opcode=0x2 (C=>S):

  - `user` ResolveToonHandleToName
    - `struct` Battlenet::Client::Profile::ResolveToonHandleToName
  - `array` m_handles
    [0x0,0x20]: range=0x21
    - `user`
      - `struct` Battlenet::Toon::Handle
        - `user` m_region
          - `user` Battlenet::Region
            - `int` Battlenet::u8
              [0x0,0xff]: range=0x100, bytes=0x1
        - `user` m_programId
          - `fourcc` Battlenet::Program::Id
        - `user` m_realm
          - `user` Battlenet::Realm::Id
            - `int` Battlenet::u32
              [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
        - `user` m_id
          - `user` Battlenet::Toon::Id
            - `int` Battlenet::u64
              [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8

## Battlenet::Client::Profile::ResolveToonHandleToNameResponse
channel=0xe, opcode=0x2 (S=>C):

  - `user` ResolveToonHandleToName
    - `struct` Battlenet::Client::Profile::ResolveToonHandleToName
  - `array` m_responses
    [0x0,0x20]: range=0x21
    - `user`
      - `struct` Battlenet::Client::Profile::HandleToNameResponse
        - `user` m_result
          - `user` Battlenet::Error::Code
            - `int` Battlenet::u16
              [0x0,0xffff]: range=0x10000, bytes=0x2
        - `user` m_handle
          - `struct` Battlenet::Toon::Handle
            - `user` m_region
              - `user` Battlenet::Region
                - `int` Battlenet::u8
                  [0x0,0xff]: range=0x100, bytes=0x1
            - `user` m_programId
              - `fourcc` Battlenet::Program::Id
            - `user` m_realm
              - `user` Battlenet::Realm::Id
                - `int` Battlenet::u32
                  [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
            - `user` m_id
              - `user` Battlenet::Toon::Id
                - `int` Battlenet::u64
                  [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8
        - `optional` m_name
          - `user`
            - `struct` Battlenet::Toon::FullName
              - `user` m_region
                - `user` Battlenet::Region
                  - `int` Battlenet::u8
                    [0x0,0xff]: range=0x100, bytes=0x1
              - `user` m_programId
                - `fourcc` Battlenet::Program::Id
              - `user` m_realm
                - `user` Battlenet::Realm::Id
                  - `int` Battlenet::u32
                    [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
              - `user` m_name
                - `string` Battlenet::Toon::Name
                  [0x2,0x19]: range=0x18
        - `optional` m_tag
          - `user`
            - `string` Battlenet::Toon::NameTag
              [0x0,0x6]: range=0x7

## Battlenet::Client::Profile::ResolveToonNameToHandleRequest
channel=0xe, opcode=0x3 (C=>S):

  - `user` ResolveToonNameToHandle
    - `struct` Battlenet::Client::Profile::ResolveToonNameToHandle
  - `user` m_name
    - `struct` Battlenet::Toon::FullName
      - `user` m_region
        - `user` Battlenet::Region
          - `int` Battlenet::u8
            [0x0,0xff]: range=0x100, bytes=0x1
      - `user` m_programId
        - `fourcc` Battlenet::Program::Id
      - `user` m_realm
        - `user` Battlenet::Realm::Id
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_name
        - `string` Battlenet::Toon::Name
          [0x2,0x19]: range=0x18

## Battlenet::Client::Profile::ResolveToonNameToHandleResponse
channel=0xe, opcode=0x3 (S=>C):

  - `user` ResolveToonNameToHandle
    - `struct` Battlenet::Client::Profile::ResolveToonNameToHandle
  - `user` m_name
    - `struct` Battlenet::Toon::FullName
      - `user` m_region
        - `user` Battlenet::Region
          - `int` Battlenet::u8
            [0x0,0xff]: range=0x100, bytes=0x1
      - `user` m_programId
        - `fourcc` Battlenet::Program::Id
      - `user` m_realm
        - `user` Battlenet::Realm::Id
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_name
        - `string` Battlenet::Toon::Name
          [0x2,0x19]: range=0x18
  - `user` m_result
    - `user` Battlenet::Error::Code
      - `int` Battlenet::u16
        [0x0,0xffff]: range=0x10000, bytes=0x2
  - `optional` m_handle
    - `user`
      - `struct` Battlenet::Toon::Handle
        - `user` m_region
          - `user` Battlenet::Region
            - `int` Battlenet::u8
              [0x0,0xff]: range=0x100, bytes=0x1
        - `user` m_programId
          - `fourcc` Battlenet::Program::Id
        - `user` m_realm
          - `user` Battlenet::Realm::Id
            - `int` Battlenet::u32
              [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
        - `user` m_id
          - `user` Battlenet::Toon::Id
            - `int` Battlenet::u64
              [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8

## Battlenet::Client::Profile::SettingsAvailable
channel=0xe, opcode=0x4 (S=>C):

  - `user` m_type
    - `enum` Battlenet::Client::Profile::SettingsType::Enum
      [0x1,0x3]: range=0x3
  - `user` m_address
    - `struct` Battlenet::Profile::RecordAddress
      - `user` m_label
        - `user` Battlenet::Label
          - `int` Battlenet::u32
            [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
      - `user` m_id
        - `user` Battlenet::Profile::RecordId
          - `int` Battlenet::u64
            [0x0,0xffffffffffffffffL]: range=0x10000000000000000L, bytes=0x8
  - `user` m_path
    - `blob` Battlenet::Profile::FieldPath
      [0x0,0x20]: range=0x21

## Battlenet::Client::Profile::ChangeSettings
channel=0xe, opcode=0x5 (C=>S):

  - `user` m_type
    - `enum` Battlenet::Client::Profile::SettingsType::Enum
      [0x1,0x3]: range=0x3
  - `user` m_settings
    - `struct` Battlenet::Profile::SettingsList
      - `array` m_stringSettings
        [0x0,0x64]: range=0x65
        - `user`
          - `struct` Battlenet::Profile::StringSetting
            - `user` m_index
              - `user` Battlenet::Profile::SettingsIndex
                - `int` Battlenet::u32
                  [0x0,0xffffffffL]: range=0x100000000L, bytes=0x4
            - `user` m_value
              - `string` Battlenet::Profile::StringType
                [0x0,0x3ff]: range=0x400
