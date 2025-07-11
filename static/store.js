  const cart = document.getElementById('cart');
  const cartItems = document.getElementById('cart-items');

  //add to cart buttons
  const buttons = document.querySelectorAll('.product-card button');

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      openCart();
      addItemToCart(button.parentElement);
    });
  });

  function openCart() {
    cart.classList.add('open');
  }

  function closeCart() {
    cart.classList.remove('open');
  }

function addItemToCart(button) {
  const name = button.getAttribute('data-name');
  const price = button.getAttribute('data-price');

  if (!name || !price) return; 

  const li = document.createElement('li');
  li.textContent = `${name} - $${price}`;
  cartItems.appendChild(li);
}


buttons.forEach(button => {
  button.addEventListener('click', () => {
    openCart();
    addItemToCart(button);
  });
});

const openCartBtn = document.getElementById('open-cart-btn');
openCartBtn.addEventListener('click', openCart);



document.addEventListener('DOMContentLoaded', function () {
  const addToCartButtons = document.querySelectorAll('.add-to-cart');

  addToCartButtons.forEach(button => {
    button.addEventListener('click', function () {
      const productCard = button.closest('.product-card');
      const productName = productCard.querySelector('h3').textContent;

      addToCart(productName);
    });
  });
});

// Add item to cart
function addToCart(productName) {
  const cartItemsList = document.getElementById('cart-items');


  const listItem = document.createElement('li');
  listItem.textContent = productName;

  // Add remove button
  const removeBtn = document.createElement('button');
  removeBtn.textContent = 'x';
  removeBtn.classList.add('remove-btn');
  removeBtn.onclick = function () {
    removeFromCart(listItem);
  };

  listItem.appendChild(removeBtn);
  cartItemsList.appendChild(listItem);
}

// Remove item from cart
function removeFromCart(itemElement) {
  itemElement.remove();
}



document.getElementById("checkout-btn").addEventListener("click", function () {
  const cartItems = document.querySelectorAll("#cart-items li");
  const itemsToBuy = [];

  cartItems.forEach(item => {
    const name = item.textContent.trim();
    itemsToBuy.push(name);
  });

  //send to flask using fetch
  fetch("/checkout", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ items: itemsToBuy }),
  })
    .then(res => res.json())
    .then(data => {
    
      
      document.getElementById("cart-items").innerHTML = "";
      const popup = document.getElementById('order-confirmed');
      popup.classList.add('show');
      setTimeout(() => {
        popup.classList.remove('show');
      }, 1200); 
    });
});


