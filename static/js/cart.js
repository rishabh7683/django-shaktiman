var updateBtns = document.getElementsByClassName('update-cart')
// here we get all our buttons
for (i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function(){ //this means on clicking on button what action should be perform
    var productId = this.dataset.product
    // this means reffering to current clicked button only , dataset means 'data' in the store.html button class, and here we actually grabbig the product id

    var action = this.dataset.action
    console.log('productId:', productId, 'Action:', action)
    console.log('USER:', user)//this we inherit from main.html
// main.html se hme user ki value pta chl gyi hai
    if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}



function addCookieItem(productId, action){
  console.log('User is not authenticated')

  if (action == 'add'){//if action is add we are increasing the value in cart
    if (cart[productId] == undefined){
      cart[productId] = {'quantity':1}//if item is not in the cart we are going to set it to 1

    }else{
      cart[productId]['quantity'] += 1//and if it is there then we are increasing it
    }
  }

  if (action == 'remove'){//if action is remove we are decreasing the value in cart
    cart[productId]['quantity'] -= 1

    if (cart[productId]['quantity'] <= 0){//if quantity is less than or equal to 0 go ahead and delete it
      console.log('Item should be deleted')
      delete cart[productId];
    }
  }
  //here what we are doing is that if page reload user does not loose the information
  console.log('CART:', cart)
  document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
//the above code is basically updating the cookie cart as button is clicked
  location.reload()
}


function updateUserOrder(productId, action){//this function basically fetch the data and send it to the view
  console.log('User is authenticated, sending data...')


  var url = '/update_item/'//we are saying this is where we want to send our data
// to send our post data we use fetch
  fetch(url, {//send data to the url
    method:'POST',//here we are going to send the post data
    headers:{
      'Content-Type':'application/json',
      //we cannot send the data directly we can send it through csrf so that's what we create here
      // we can send our data to views.py through main.html get token function which is about csrf token
      'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({'productId':productId, 'action':action})//it will send th product id and action to our backend which is our view
  })//this is what we send the data , once we send data we want promise that data view ko pahuch gya hai to hme view se response milega Item was added //return JsonResponse('Item was added',
  .then((response) => {
     return response.json();
  })
  .then((data) => {
  //  console.log('Data', data)
    location.reload()
    });
}
