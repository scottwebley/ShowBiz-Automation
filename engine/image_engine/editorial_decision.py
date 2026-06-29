"""
===========================================
ShowBiz Image Engine
editorial_decision.py
Version 1.0
===========================================

Represents the AI Editor's decision.

This object is passed throughout the
Image Engine instead of raw dictionaries.
"""

from dataclasses import dataclass


@dataclass
class EditorialDecision:

    subject: str

    subject_type: str

    story_type: str

    preferred_photo: str

    preferred_source: str

    reasoning: str


if __name__ == "__main__":

    decision = EditorialDecision(

        subject="Taylor Swift",

        subject_type="person",

        story_type="concert appearance",

        preferred_photo="performance",

        preferred_source="editorial_photo",

        reasoning="Taylor Swift is the primary visual subject."

    )

    print(decision)