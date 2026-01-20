from .utils import get_or_create_cart


def cart_context(request):
    """Добавляет в контекст шаблонов информацию о корзине для текущего пользователя.

    Возвращает словарь с `cart_total_items` и `cart_total_price`.
    Если пользователь не аутентифицирован — значения будут равны 0.
    """
    cart_total_items = 0
    cart_total_price = 0

    if request.user.is_authenticated:
        cart = get_or_create_cart(request.user)
        cart_total_items = cart.total_items
        cart_total_price = cart.total_price

    return {
        'cart_total_items': cart_total_items,
        'cart_total_price': cart_total_price,
    }
