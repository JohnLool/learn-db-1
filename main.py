from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User, Product, Order
from database import get_db, init_db, delete_db
from typing import List, Annotated
from contextlib import asynccontextmanager
from schemas import UserCreate, UserRead, ProductCreate, ProductRead, OrderCreate, OrderRead
from auth import router as auth_router, get_password_hash


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_db()
    print("База очищена")
    await init_db()
    print("База создана")
    yield
    print("Выключение")

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)


@app.post("/users/", response_model=UserCreate)
async def create_user(user: Annotated[UserCreate, Depends()], db: AsyncSession = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


# Создание нового продукта
@app.post("/products/", response_model=ProductCreate)
async def create_product(product: Annotated[ProductCreate, Depends()], db: AsyncSession = Depends(get_db)):
    db_product = Product(name=product.name, price=product.price)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


@app.get("/products/", response_model=List[ProductRead])
async def read_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products


@app.post("/orders/")
async def create_order(order: Annotated[OrderCreate, Depends()], db: AsyncSession = Depends(get_db)):
    db_order = Order(user_id=order.user_id, product_id=order.product_id)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return {"order_id": db_order.id}


@app.get("/orders/", response_model=List[OrderRead])
async def read_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order))
    orders = result.scalars().all()
    return orders


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
