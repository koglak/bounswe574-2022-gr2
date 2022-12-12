// window.onload = function() {
//     if (window.jQuery) {
//        alert('jQuery is loaded');
//     } else {
//        alert('jQuery is not loaded');
// }}

function getSelectedText(e) {
    var selection = window.getSelection().getRangeAt(0);
    if(window.getSelection().toString().length != 0){
        $("#popup").css("visibility", "visible");
        $("#popup").css("position", "absolute");
        
        var left=JSON.stringify(event.pageX-5)+"px"
        var top=JSON.stringify(event.pageY-60)+"px"
        $("#popup").css("top", top);
        $("#popup").css("left", left );
    }
    var selectedText = selection.extractContents();
    // alert(selectedText.textContent);
    var span = $("<span class='selected'>" + selectedText.textContent + "</span>");
    selection.insertNode(span[0]);
  
  }

  $(document).ready(function(){
    $('p').mouseup(function(event) {
        getSelectedText()
       
      });
      
      $('p').mousedown(function() {
        // $(this).find('.selected').contents().unwrap();
        $("#popup").css("visibility", "hidden");
      });

   
   
  });
 