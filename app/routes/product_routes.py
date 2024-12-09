from typing import Annotated
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Import service functions
from app.services.product_service import *
from app.services.category_service import getAllCategories

from app.models.product import Product

router = APIRouter()

# Set location for templates
templates = Jinja2Templates(directory="app/view_templates")

# Handle HTTP GET requests for the site root /
@router.get("/", response_class=HTMLResponse)
async def getProducts(request: Request):
    products = getAllProducts()  # Fetch all products with category names
    categories = getAllCategories()  # Fetch all categories

    # Pass products and categories to the page
    return templates.TemplateResponse(
        "product/products.html",
        {"request": request, "products": products, "categories": categories}
    )

# Handle HTTP GET requests for the product update form
@router.get("/update/{id}", response_class=HTMLResponse)
async def getProductUpdateForm(request: Request, id: int):
    product = getProduct(id)  # Fetch product by ID
    categories = getAllCategories()  # Fetch all categories for dropdown

    # Pass product and categories to the update form
    return templates.TemplateResponse(
        "product/partials/product_update_form.html",
        {"request": request, "product": product, "categories": categories}
    )

# Handle HTTP PUT requests to update a product
@router.put("/")
def putProduct(request: Request, productData: Annotated[Product, Form()]):
    updated_product = updateProduct(productData)  # Update the product and fetch it with category
    return templates.TemplateResponse(
        "product/partials/product_tr.html",
        {"request": request, "product": updated_product}
    )

# Handle HTTP POST requests to add a product
@router.post("/")
def postProduct(request: Request, productData: Annotated[Product, Form()]):
    new_product = newProduct(productData)  # Add the new product

    # Attach category name to the product for the UI
    categories = getAllCategories()
    category_name = next(
        (c["name"] for c in categories if c["id"] == new_product["category_id"]), "Unknown"
    )
    new_product["category"] = {"name": category_name}

    return templates.TemplateResponse(
        "product/partials/product_tr.html",
        {"request": request, "product": new_product}
    )

# Handle HTTP DELETE requests to delete a product
@router.delete("/{id}")
def delProduct(request: Request, id: int):
    deleteProduct(id)  # Delete the product by ID
    return templates.TemplateResponse(
        "product/partials/product_list.html",
        {"request": request, "products": getAllProducts()}
    )

# Handle HTTP GET requests to filter products by category
@router.get("/bycat/{id}", response_class=HTMLResponse)
def getProductsByCategory(request: Request, id: int):
    products = getProductByCat(id)  # Fetch products filtered by category
    return templates.TemplateResponse(
        "product/partials/product_list.html",
        {"request": request, "products": products}
    )
