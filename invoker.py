from commands import SayHelloCommand, CreateUserGroupCommand, LoginCommand, CreateUserCommand, LogoutCommand, \
    RefreshTokenCommand, MeCommand

command_registry = [
    CreateUserCommand(),
    LoginCommand(),
    SayHelloCommand(),
    CreateUserGroupCommand(),
    RefreshTokenCommand(),
    LogoutCommand(),
    MeCommand()

]
