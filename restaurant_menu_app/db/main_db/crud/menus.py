from sqlalchemy import distinct, func  # , insert, select

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from restaurant_menu_app.models import model
from restaurant_menu_app.schemas import scheme


def read_menus(db: Session):
    return db.query(
        model.Menu.id,
        model.Menu.title,
        model.Menu.description,
        func.count(distinct(model.Submenu.id)).label('submenus_count'),
        func.count(model.Dish.id).label('dishes_count'),
    ).join(
        model.Submenu,
        model.Submenu.menu_id == model.Menu.id,
        isouter=True,
    ).join(
        model.Dish,
        model.Dish.submenu_id == model.Submenu.id,
        isouter=True,
    ).group_by(model.Menu.id).all()


def read_menu(menu_id: str, db: Session):
    return db.query(
        model.Menu.id,
        model.Menu.title,
        model.Menu.description,
        func.count(distinct(model.Submenu.id)).label('submenus_count'),
        func.count(model.Dish.id).label('dishes_count'),
    ).join(
        model.Submenu,
        model.Submenu.menu_id == model.Menu.id,
        isouter=True,
    ).join(
        model.Dish,
        model.Dish.submenu_id == model.Submenu.id,
        isouter=True,
    ).filter(
        model.Menu.id == menu_id,
    ).group_by(model.Menu.id).first()


def read_menu_by_title(menu_title: str, db: Session):
    return db.query(model.Menu).filter(
        model.Menu.title == menu_title,
    ).first()


def create_menu(data: scheme.MenuCreate, db: Session):
    new_menu = model.Menu(**data.dict())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu.id
    # return read_menu(menu.id, db)


def update_menu(menu_id: str, patch: scheme.MenuUpdate, db: Session):
    db.query(model.Menu).filter(
        model.Menu.id == menu_id,
    ).update(patch.dict())
    db.commit()


def delete_menu(menu_id: str, db: Session):
    menu = db.query(model.Menu).filter(model.Menu.id == menu_id).first()
    db.delete(menu)
    db.commit()