from dataclasses import dataclass
from drafter import *

hide_debug_information()
set_website_title("Drafter Calculator")
set_site_information(author = "Lucy Reese", description = "calculate numbers using add, subtract, multiply, or divide.", sources = "", planning = "", links = [""])
set_website_framed(False)

@dataclass
class History:
    nums: list[float]
    operation: str
    total: float


@dataclass
class State:
    total: float
    old: list[History]
    title: str
    counter: int


@route
def index(state: State) -> Page:
    """Show the main calculator page."""
    return Page(state, [
        Header("My Calculator"),
        "Welcome to your personal calculator!",
        "Enter two numbers and choose an operation.",
        
        Header("Calculator", 2),

        "First number:",
        TextBox("first_number", 0.0, "number"),

        "Second number:",
        TextBox("second_number", 0.0, "number"),

        "Choose an operation:",
        SelectBox("operation",
                  ["Add", "Subtract", "Multiply", "Divide"],
                  state.title),

        Button("Calculate", "calculate"),

        Header("Your Result", 2),
        "Current answer: " + str(state.total),
        "Number of calculations: " + str(state.counter),
        
        Button("View History", "history"),
        
        Button("Complex Math", "complex_math"),
        
        Button("Greek Letters", "greek_letters")
    ])


@route
def calculate(state: State, first_number: float,
              second_number: float, operation: str) -> Page:
    """Calculate the answer and save the calculation to history."""

    if operation == "Add":
        state.total = first_number + second_number

    elif operation == "Subtract":
        state.total = first_number - second_number

    elif operation == "Multiply":
        state.total = first_number * second_number

    elif operation == "Divide":
        if second_number == 0:
            state.title = operation
            return Page(state, [
                Header("Error"),
                "You cannot divide by zero!",
                Button("Go Back", "index")
            ])
        else:
            state.total = first_number / second_number

    state.title = operation
    state.counter += 1

    state.old.append(
        History([first_number, second_number],
                operation, state.total)
    )

    if state.counter % 20 == 0:
        return surprise(state)
    else:
        return index(state)

@route
def history(state: State) -> Page:
    """Display the user's previous calculations."""

    content = [
        Header("Calculation History"),
        "Here are all of your previous calculations!"
    ]

    if len(state.old) == 0:
        content.append("You haven't completed any calculations yet.")

    else:
        for item in state.old:
            content.append(Header("Calculation", 2))
            content.append("Numbers: " + str(item.nums))
            content.append("Operation: " + item.operation)
            content.append("Answer: " + str(item.total))

    content.append(Button("Back to Calculator", "index"))
    content.append(Button("Clear History", "clear_history"))

    return Page(state, content)


@route
def clear_history(state: State) -> Page:
    """Remove all previous calculations from history."""

    state.old = []

    return history(state)


@route
def complex_math(state: State) -> Page:
    """Display the complex math calculator."""

    return Page(state, [
        Header("Complex Math Calculator"),
        "Use three numbers to complete a calculation.",

        "First number:",
        TextBox("first_number", 0.0, "number"),

        "Second number:",
        TextBox("second_number", 0.0, "number"),

        "Third number:",
        TextBox("third_number", 0.0, "number"),

        "Choose an operation:",
        SelectBox("operation",
                  ["Add", "Subtract", "Multiply", "Divide"],
                  "Add"),

        Button("Calculate", "complex_calculate"),

        Button("Back to Calculator", "index"),
        Button("View History", "history")
    ])


@route
def complex_calculate(state: State, first_number: float,
                      second_number: float, third_number: float,
                      operation: str) -> Page:
    """Calculate an operation using three numbers."""

    if operation == "Add":
        state.total = first_number + second_number + third_number

    elif operation == "Subtract":
        state.total = first_number - second_number - third_number

    elif operation == "Multiply":
        state.total = first_number * second_number * third_number

    elif operation == "Divide":
        if second_number == 0 or third_number == 0:
            return Page(state, [
                Header("Error"),
                "You cannot divide by zero!",
                Button("Try Again", "complex_math")
            ])
        else:
            state.total = first_number / second_number / third_number

    state.title = "Complex " + operation
    state.counter += 1

    state.old.append(
        History(
            [first_number, second_number, third_number],
            state.title,
            state.total
        )
    )

    if state.counter % 20 == 0:
        return surprise(state)
    else:
        return Page(state, [
        Header("Complex Math Result"),
        "Operation: " + state.title,
        "Numbers: " + str(first_number) + ", " +
        str(second_number) + ", " + str(third_number),
        "Answer: " + str(state.total),

        Button("Calculate Again", "complex_math"),
        Button("Back to Calculator", "index"),
        Button("View History", "history")
    ])

@route
def greek_letters(state: State) -> Page:
    """Display common Greek letters used in mathematics."""

    return Page(state, [
        Header("Greek Letters"),
        "Use this page to find Greek symbols for your math problems!",

        Header("Lowercase Greek Letters", 2),

        "Alpha: α",
        "Beta: β",
        "Gamma: γ",
        "Delta: δ",
        "Epsilon: ε",
        "Theta: θ",
        "Lambda: λ",
        "Mu: μ",
        "Pi: π",
        "Sigma: σ",
        "Omega: ω",

        Header("Uppercase Greek Letters", 2),

        "Alpha: Α",
        "Beta: Β",
        "Gamma: Γ",
        "Delta: Δ",
        "Theta: Θ",
        "Lambda: Λ",
        "Pi: Π",
        "Sigma: Σ",
        "Omega: Ω",

        Header("Common Mathematical Uses", 2),

        "π (Pi): Used in circle calculations.",
        "Δ (Delta): Represents a change in a value.",
        "θ (Theta): Often represents an angle.",
        "Σ (Sigma): Represents a sum.",
        "λ (Lambda): Often used for variables or constants.",

        Button("Back to Calculator", "index"),
        Button("Complex Math", "complex_math"),
        Button("View History", "history")
    ])

@route
def surprise(state: State) -> Page:
    """Show a surprise message after every 20 calculations."""

    return Page(state, [
        Header("🎉 SURPRISE! 🎉"),
        "You have used this calculator "
        + str(state.counter) + " times!",
        "Thanks for using my calculator!",

        Button("Back to Calculator", "index"),
        Button("Try Complex Math", "complex_math")
    ])

start_server(State(0.0, [], "Add", 0))
