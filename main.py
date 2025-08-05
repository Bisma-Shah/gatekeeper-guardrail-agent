import asyncio
import rich
from pydantic import BaseModel
from connection import config
from agents import (
    Agent,
    Runner,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered
)

# -------------------- Output Model --------------------
class GateEntry(BaseModel):
    message: str
    isOtherSchool: bool


# -------------------- Gatekeeper Agent --------------------
gatekeeper_agent = Agent(
    name="GIAIC Gatekeeper",
    instructions=(
        """
        Only allow students from GIAIC.
        If the student is from any other institute, block their entry.
        """
    ),
    output_type=GateEntry
)


# -------------------- Guardrail Function --------------------
@input_guardrail
async def gatekeeper_guardrail(ctx, agent, input):
    result = await Runner.run(
        gatekeeper_agent,
        input,
        context=ctx
    )
    rich.print(result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output.message,
        tripwire_triggered=result.final_output.isOtherSchool
    )


# -------------------- Student Agent --------------------
student_agent = Agent(
    name="Student Agent",
    instructions="You are a student trying to enter GIAIC.",
    input_guardrails=[gatekeeper_guardrail]  
)


# -------------------- Main Function --------------------
async def main():
    try:
        result = await Runner.run(
            student_agent,
            "Hi! I am from GIAIC Coding Academy.",
            run_config=config
        )
        rich.print("Student entered GIAIC.")

    except InputGuardrailTripwireTriggered:
        print("Gatekeeper blocked the student. Not from GIAIC!")


# -------------------- Entry Point --------------------
if __name__ == "__main__":
    asyncio.run(main())
