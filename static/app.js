async function get_cupcakes() {
  const res = await axios.get('/api/cupcakes');
  const cupcakes = res.data.cupcakes;
  return cupcakes
}

function add_cupcake(cupcake){
  let $new_li = $('<li>');
  $new_li.text(`${cupcake.flavor}, ${cupcake.size} - ${cupcake.rating}/10`);
  $('ul').append($new_li);
}

$(document).ready(async function(){
  const cupcakes = await get_cupcakes();
  cupcakes.forEach(cupcake => add_cupcake(cupcake));
});

$('form').submit(async function(e){
  e.preventDefault();
  form_data = {
      flavor: $("input[data-type='flavor']").val(),
      size: $("input[data-type='size']").val(),
      rating: $("input[data-type='rating']").val(),
      img_url: $("input[data-type='img_url']").val()
  };

  await axios.post( "/api/cupcakes", form_data );
  add_cupcake(form_data)
});