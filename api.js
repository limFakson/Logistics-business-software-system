const email = document.getElementById('email')
const wallet = document.getElementById('wallet')

fetch('https://api-fluidpay.onrender.com/wallets/')
.then(response=>{
    if(!response.ok){

    }
    return response.json();
})
.then(data=>{
    data.forEach((value, index, array) => {
        email.textContent = value.email
        wallet.textContent=value.wallet
    })
    console.log(data)
})
.catch(error=> {
    console.error(error)
})