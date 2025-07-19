from commands import SayHelloCommand, CreateUserGroupCommand, LoginCommand, CreateUserCommand

command_registry = [
    CreateUserCommand(),
    LoginCommand(),
    SayHelloCommand(),
    CreateUserGroupCommand(),

]
