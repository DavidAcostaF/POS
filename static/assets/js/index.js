;(function(){
    const modal = new bootstrap.Modal(document.getElementById('modals'))

    htmx.on('htmx:afterSwap',(e)=>{
        if (e.detail.target.id === "dialog")
        modal.show()
    })
    
    htmx.on('htmx:beforeSwap',(e)=>{
        if (e.detail.target.id === "dialog" && !e.detail.xhr.response)
        modal.hide()
    })

})()


function deleteInventory(id){
    const modal = new bootstrap.Modal(document.getElementById('modal'))
    modal.show()
    form = document.getElementById('form_delete')
    form.action = `/products/delete_inventory/${id}`
}


function addToCar(id){
    $.ajax({
        type:'post',
        url: `products/add_car/${id}`,
        data:{
            'id':id,csrfmiddlewaretoken:$("[name = 'csrfmiddlewaretoken']").val()
        },
        success: function(data) {
            console.log(data); 
        }
    })
}

const updateQuantity = (id)=>{
    let quantity = document.getElementById(`quantity_${id}`).value
    let cost = Number(document.getElementById(`cost_${id}`).textContent)
    let subtotal = document.getElementById(`subtotal_${id}`)
    let product = document.getElementById(`product_${id}`)
    elementTotal = document.getElementById('total')
    let total = 0
    let sum = 0
    if(quantity != 0){
        $.ajax({
            url:`/products/update_quantity/${id}`,
            type:"post",
            dataType:'json',
            data:{csrfmiddlewaretoken:$("[name = 'csrfmiddlewaretoken']").val(),'quantity':quantity},
            success:function(){
                subtotal.innerHTML = quantity*cost
            }
        })
    }else{
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url:`/products/update_quantity/${id}`,
                    type:"post",
                    dataType:'json',
                    data:{csrfmiddlewaretoken:$("[name = 'csrfmiddlewaretoken']").val(),'quantity':quantity},
                    success:function(){
                        product.innerHTML = ""
                    }
                })
              Swal.fire(
                'Deleted!',
                'Your file has been deleted.',
                'success'
                )
            }else{
                quantity = document.getElementById(`quantity_${id}`).value = 1
            }
        })
    }
    let column = document.querySelectorAll('.sub_total')
    column.forEach(e=>{
        total = Number(e.textContent)
        sum += total
    })
    elementTotal.innerHTML = sum
}


function addToCarWithQuantity(id){
    quantity = document.getElementById('input').value
    if (quantity > 0){
        $.ajax({
            type:'post',
            url: `/products/add_with_quantity/${id}`,
            data:{
                'id':id,csrfmiddlewaretoken:$("[name = 'csrfmiddlewaretoken']").val(),'input':quantity
            },
            success: function(data) {
                window.location.reload()
            }
        })
    }
}


const deleteInCart = (id) =>{
    let product = document.getElementById(`product_${id}`)
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url:`/products/delete_in_cart/${id}`,
                    type:"post",
                    dataType:'json',
                    data:{csrfmiddlewaretoken:$("[name = 'csrfmiddlewaretoken']").val()}
                })
            product.innerHTML = ""
            Swal.fire(
                'Deleted!',
                'Your file has been deleted.',
                'success'
                )
            }
        })
    }


function alertActivate(){
    Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Something went wrong!',
        footer: '<a href="">Login or Activate account</a>',
    })
}
