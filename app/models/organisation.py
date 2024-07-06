from ..extensions import db
import uuid


"""Association table"""
users_organisation = db.Table("users_organisation", 
        db.Column("organisation_id", db.String, db.ForeignKey("organisations.orgId")),
        db.Column("user_id", db.String, db.ForeignKey("users.userId"))
    )

class Organisation(db.Model):
    """Models an organisation"""
    __tablename__ = "organisations"
    orgId = db.Column(db.String, primary_key=True, unique=True, index=True, nullable=False)
    name = db.Column(db.String, unique=True, index=True, nullable=False)
    description = db.Column(db.Text)

    users = db.relationship("User",
                            secondary=users_organisation,
                            backref=db.backref("organisations", lazy="dynamic"),
                            lazy="dynamic"
                            )

    def __init__(self, *args, **kwargs) -> None:
        super(Organisation, self).__init__(*args, **kwargs)
        self.orgId = str(uuid.uuid4())

    def __repr__(self) -> str:
        return f'<Organisation_name {self.name}>'
    
    """Validations"""
    def validate_org(self):
        errors = []
        if not self.name or len(self.name) < 3:
            resp = {
                "field": "name",
                "message": "Organisation's name cannot be null or less than 3 characters"
            }
            errors.append(resp)
        return errors

