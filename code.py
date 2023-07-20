 else:
        cart_contents = request.session.get('cart', {})

        # Fetch additional product details for non-authenticated users
        cart_contents_with_details = []
        for slug, quantity in cart_contents.items():
            product = get_object_or_404(Product, slug=slug)
            cart_item_with_details = {
                "product_name":product.name,
                "img":product.img1.url,
                "price":product.price if product.discount == 0 else product.discount_price,
                "quantity":quantity,
                "slug":product.slug,
                "in_stock":product.in_stock()
            }
            cart_contents_with_details.append(cart_item_with_details)
        cart_contents = cart_contents_with_details
        cart_contents = cart_contents_with_details
        number_of_items=0
        total_amt=0
        for item in cart_contents_with_details:
            number_of_items += item['quantity']
    
    print(cart_contents)