var cart = [];

function addToCart(itemId, itemName, itemPrice) {
  var quantity = document.getElementById("quantity_" + itemId).value;
  var item = {
    id: itemId,
    name: itemName,
    price: itemPrice,
    quantity: quantity,
  };
  cart.push(item);
  updateCartInfo();
}

function updateCartInfo() {
  var cartInfoDiv = document.getElementById("cartInfo");
  cartInfoDiv.innerHTML = "<h2>購物車</h2>";
  for (var i = 0; i < cart.length; i++) {
    cartInfoDiv.innerHTML +=
      "<p>" +
      cart[i].name +
      " - 數量：" +
      cart[i].quantity +
      " - $" +
      cart[i].price * cart[i].quantity +
      "</p>";
  }
}

function checkout() {
  // 將購物車資訊提交到後台
  fetch("/checkout", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(cart),
  })
    .then((response) => response.json())
    .then((data) => {
      alert("結帳成功！");
      // 清空購物車
      cart = [];
      updateCartInfo();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
