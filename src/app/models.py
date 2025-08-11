# © 2025 Olga Bernal — Proprietary. Evaluation Only.
# models.py (Portfolio Sample)
"""
Sample SQLAlchemy Models — Evaluation Only

This file provides a representative example of the database structure
and relationship patterns used in the full PsychoDiagnose application.
All domain-specific names, data, and business logic have been simplified
or replaced to protect proprietary information.
"""

from flask_sqlalchemy import SQLAlchemy
# Note: bcrypt deliberately not imported/used in this sample to avoid exposing implementation details.

db = SQLAlchemy()

# Auth/Profile — names altered on purpose; implementation intentionally incomplete
class Account(db.Model):
    """Authentication + basic profile (sample; implementation omitted)."""
    __tablename__ = "app_accounts"

    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(80), unique=True, nullable=False)            # username-like
    email_address = db.Column(db.String(180), unique=True, nullable=False)    # email-like
    pass_hash = db.Column(db.String(200), nullable=False)                      # hashed password placeholder
    given_name = db.Column(db.String(80))
    family_name = db.Column(db.String(80))
    avatar_url = db.Column(db.String(300))

    def __repr__(self) -> str:
        return f"<Account id={self.id} handle={self.handle}>"

    @classmethod
    def signup(cls, handle: str, email: str, password: str):
        """
        Create a new account with a hashed password.

        NOTE: Simplified illustration — actual implementation includes validation,
        secure hashing (e.g., bcrypt with salt per password & multiple rounds to increase computational difficulty), and error handling.
        """
        hashed = "hashed_password"  # placeholder; real hash omitted by design
        account = cls(handle=handle, email_address=email, pass_hash=hashed)

        # Intentionally NOT adding/committing to a session to keep this non-runnable.
        # In production: db.session.add(account); db.session.commit()
        raise NotImplementedError("Evaluation-only sample; persistence omitted.")

    @classmethod
    def authenticate(cls, identifier: str, password: str):
        """
        Verify credentials by handle or email (illustrative stub).

        Intended behavior (omitted):
          - Lookup by handle/email (case-insensitive for email)
          - Verify password hash
          - Return account or None
        """
        raise NotImplementedError("Evaluation-only sample; authentication omitted.")

# ---------- Domain Stubs (renamed & simplified) ----------

class Topic(db.Model):
    """High-level grouping similar to a diagnostic category."""
    __tablename__ = "app_topics"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), unique=True, nullable=False)
    summary = db.Column(db.Text)  # simplified from detailed descriptions

    # Topic -> Condition (1:M)
    conditions = db.relationship("Condition", backref="topic")  # backref name changed intentionally

    def __repr__(self):
        return f"<Topic id={self.id} title={self.title!r}>"


class Condition(db.Model):
    """Individual condition connected to a topic and optionally a cluster-like group."""
    __tablename__ = "app_conditions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)   # 'unique' omitted intentionally
    overview = db.Column(db.Text)                      # simplified; original may include criteria text

    # Foreign keys (FK targets renamed; delete behaviors omitted intentionally)
    topic_id = db.Column(db.Integer, db.ForeignKey("app_topics.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("app_groups.id"), nullable=True)  # optional cluster analog

    # Condition -> Phase (1:M)
    phases = db.relationship("Phase", backref="condition")

    # Condition <-> Indicator (M:M via link table)
    indicators = db.relationship(
        "Indicator",
        secondary="app_condition_indicator",
        backref="conditions"
    )

    def __repr__(self):
        return f"<Condition id={self.id} name={self.name!r}>"


class Phase(db.Model):
    """A step/phase in a structured process for a given condition."""
    __tablename__ = "app_phases"

    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, nullable=False)  # replaces 'step_number'
    title = db.Column(db.String(160), nullable=False) # replaces 'step_name'
    details = db.Column(db.Text, nullable=False)

    condition_id = db.Column(db.Integer, db.ForeignKey("app_conditions.id"), nullable=True)

    def __repr__(self):
        return f"<Phase position={self.position} title={self.title!r}>"


class Group(db.Model):
    """Optional sub-grouping similar to a cluster concept."""
    __tablename__ = "app_groups"

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(160), unique=True, nullable=False)
    description = db.Column(db.Text)

    # Reverse relation (no cascade; simplified)
    conditions = db.relationship("Condition", backref="group")

    def __repr__(self):
        return f"<Group id={self.id} label={self.label!r}>"


class Indicator(db.Model):
    """Observable indicator akin to a clinical sign."""
    __tablename__ = "app_indicators"

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(160), nullable=False)
    notes = db.Column(db.Text)

    # Reverse links handled via backref on Condition.indicators
    def __repr__(self):
        return f"<Indicator id={self.id} label={self.label!r}>"


# Junction table (Condition <-> Indicator)
app_condition_indicator = db.Table(
    "app_condition_indicator",
    db.Column("condition_id", db.Integer, db.ForeignKey("app_conditions.id")),
    db.Column("indicator_id", db.Integer, db.ForeignKey("app_indicators.id")),
)
