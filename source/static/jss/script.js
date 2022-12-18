function clicked_img(img,fp){
          var top=document.getElementById('top')
          top.src = img.src;
          top.hidden=false;

          if (img.naturalWidth<screen.width*0.6 && img.naturalHeight<screen.height*0.6) {

            top.width=img.naturalWidth;
            top.height=img.naturalHeight;

          } else {
            top.width=screen.width*0.6;
            top.height=img.naturalHeight/img.naturalWidth*top.width;
          }
          document.getElementById('close').hidden = false;
          document.getElementById('delete').hidden = false;
 }


function do_close(){
  document.getElementById('top').hidden=true;
  document.getElementById('close').hidden=true;
  document.getElementById('delete').hidden=true;
}

function do_delete(){
    var top=document.getElementById('top')
    console.log(top.src);
    $.ajax( {
        url: '/photo/delete',
        type: 'POST',
        data: {
                image_path: top.src
        },
        success: function ( response ) {
            debugger;
              document.getElementById('top').hidden=true;
              document.getElementById('close').hidden=true;
              document.getElementById('delete').hidden=true;

              response_json = JSON.parse(response)
              const img = document.getElementById(response_json.id);
              img.setAttribute('src', '');
              img.style.display = 'none';
        },
        error: function ( response ) {
                console.log(response)
        }
} );



}