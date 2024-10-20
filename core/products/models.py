"""
Definition of models for the `inventory` app.
"""

from uuid import uuid4

from django.db import models


class Attribute(models.Model):
    """
    Model that describes the Attribute model.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(null=True)


class AttributeValue(models.Model):
    """
    Model describing a values for the Attribute model.
    """

    value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute,
        related_name="values",
        on_delete=models.CASCADE,
    )


class Category(models.Model):
    """
    Model describing the category model
    """

    name = models.CharField(
        unique=True,
        max_length=100,
    )
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.PROTECT,
    )


class SeasonalEvent(models.Model):
    """
    Model describing seasonal events.
    """

    # Auto incrementing field that is set as the primary key
    id = models.BigAutoField(primary_key=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(
        unique=True,
        max_length=100,
    )


class ProductType(models.Model):
    """
    Model that describes the ProductType model.
    """

    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        related_name="types",
        on_delete=models.CASCADE,
    )


class Product(models.Model):
    """
    Model describing a single Product instance.
    """

    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"

    STOCK_STATUS = {
        IN_STOCK: "In stock",
        OUT_OF_STOCK: "Out of stock",
    }

    # Defining the max length of char fields allows DBs to allocate
    # the appropriate amount of space for the data to be stored
    pid = models.CharField(
        unique=True,
        max_length=255,
    )

    slug = models.SlugField(unique=True)

    name = models.CharField(
        unique=True,
        max_length=255,
    )
    description = models.TextField(null=True)

    is_active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
    )
    seasonal_event = models.ForeignKey(
        SeasonalEvent,
        null=True,
        related_name="products",
        on_delete=models.SET_NULL,
    )


class ProductProductType(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
    )


class ProductLine(models.Model):
    """
    Model describing a single product line instance.
    """

    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.UUIDField(
        default=uuid4,
        unique=True,
    )
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    order = models.IntegerField()
    weight = models.FloatField()
    product = models.ForeignKey(
        Product,
        related_name="product_lines",
        on_delete=models.PROTECT,
    )

    class Meta:
        """
        Meta for the ProductLine model.
        """

        verbose_name = "Product Line"
        verbose_name_plural = "Product Lines"


class ProductLineAttribute(models.Model):
    value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
    )
    product_line = models.ForeignKey(
        ProductLine,
        on_delete=models.CASCADE,
    )


class ProductImage(models.Model):
    """
    Model describing a product image.
    """

    name = models.CharField(max_length=100)
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField()
    product_line = models.ForeignKey(
        ProductLine,
        related_name="images",
        on_delete=models.CASCADE,
    )
    default_image = models.BooleanField(
        default=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product_line"],
                condition=models.Q(default_image=True),
                name="unique_default_image_per_product_line",
            )
        ]
