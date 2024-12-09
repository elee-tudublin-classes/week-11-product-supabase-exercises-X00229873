# import the model class
from app.models.product import Product
from starlette.config import Config
from supabase import create_client, Client

# Load environment variables from .env
config = Config(".env")

db_url: str = config("SUPABASE_URL")
db_key: str = config("SUPABASE_KEY")

supabase: Client = create_client(db_url, db_key)

# get all products with category name
def dataGetProducts():
    response = (
        supabase.table("product")
        .select("*, category(name)")  # Include category name
        .order("title", desc=False)  # Order by title
        .execute()
    )
    return response.data

# get product by id with category name
def dataGetProduct(id):
    response = (
        supabase.table("product")
        .select("*, category(name)")  # Include category name
        .eq("id", id)  # Filter by ID
        .execute()
    )
    return response.data[0]

# get products filtered by category ID
def dataGetProductByCat(category_id: int):
    response = (
        supabase.table("product")
        .select("*, category(name)")  # Include category name
        .eq("category_id", category_id)  # Filter by category ID
        .order("title", desc=False)  # Order by title
        .execute()
    )
    return response.data

# update product
def dataUpdateProduct(product: Product):
    response = (
        supabase.table("product")
        .upsert(product.dict())  # Convert product object to dict for Supabase
        .execute()
    )
    return response.data[0]

# add product, accepts product object
def dataAddProduct(product: Product):
    response = (
        supabase.table("product")
        .insert(product.dict())  # Convert product object to dict for Supabase
        .execute()
    )
    return response.data[0]

# get all categories
def dataGetCategories():
    response = (
        supabase.table("category")
        .select("*")  # Get all fields from category
        .order("name", desc=False)  # Order by name
        .execute()
    )
    return response.data

# delete product by id
def dataDeleteProduct(id):
    response = (
        supabase.table("product")
        .delete()
        .eq("id", id)  # Filter by ID
        .execute()
    )
    return response.data
