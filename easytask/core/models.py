"""Models."""
import datetime as dt

from sqlalchemy import orm
from sqlalchemy.exc import IntegrityError

from .database import db


class BaseModel(db.Model):
    """Base model."""

    __abstract__ = True

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: dt.datetime.now(dt.timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        onupdate=lambda: dt.datetime.now(dt.timezone.utc),
        nullable=True,
    )

    @classmethod
    def eager(cls, *args):
        """Eagerly load data."""
        cols = [orm.joinedload(arg) for arg in args]
        return cls.query.options(*cols)

    @classmethod
    def before_bulk_create(cls, iterable, *args, **kwargs):
        """Before bulk create hook."""

    @classmethod
    def after_bulk_create(cls, model_objs, *args, **kwargs):
        """After bulk create hook."""

    @classmethod
    def bulk_create(cls, iterable, *args, **kwargs):
        """Bulk create instances."""
        cls.before_bulk_create(iterable, *args, **kwargs)
        model_objs = []

        for data in iterable:
            if not isinstance(data, cls):
                data = cls(**data)
            model_objs.append(data)

        db.session.bulk_save_objects(model_objs)
        if kwargs.get('commit', True) is True:
            db.session.commit()

        cls.after_bulk_create(model_objs, *args, **kwargs)
        return model_objs

    @classmethod
    def bulk_create_or_none(cls, iterable, *args, **kwargs):
        """Bulk create instances or rollback."""
        try:
            return cls.bulk_create(iterable, *args, **kwargs)
        except IntegrityError:
            db.session.rollback()
            return None

    def before_save(self, *args, **kwargs):
        """Before save hook."""

    def after_save(self, *args, **kwargs):
        """After save hook."""

    def save(self, commit=True):
        """Save instance."""
        self.before_save()
        db.session.add(self)

        if commit:
            try:
                db.session.commit()
            except Exception as err:
                db.session.rollback()
                raise err

        self.after_save()

    def before_update(self, *args, **kwargs):
        """Before update hook."""

    def after_update(self, *args, **kwargs):
        """After update hook."""

    def update(self, *args, **kwargs):
        """Update instance."""
        self.before_update(*args, **kwargs)
        db.session.commit()
        self.after_update(*args, **kwargs)

    def delete(self, commit=True):
        """Delete instance."""
        db.session.delete(self)
        if commit:
            db.session.commit()
