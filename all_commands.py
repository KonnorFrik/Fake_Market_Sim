from commands_handler import register # last in import section
import settings


@register
def info(name, *a, **kw):
    """Show info about given object"""
    if (type_ := type(name)) is not list and type_ is not str and name is not None:
        print(name)

    else:
        print("No argument for display")


#if __name__ == "__main__":
    #info("hello")
    #info(["hello"])

