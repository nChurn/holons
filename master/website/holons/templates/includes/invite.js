<script>
  $(document).ready(function(){
    setInviteBt()
    $.ajaxSetup({
     beforeSend: function(xhr, settings) {
       xhr.setRequestHeader("X-CSRFToken", window.csrftoken);
     }
    });
    function setInviteBt () {
      $('#generateCodeBt').on('click', function(event){
        activateCodeField()
        getInvitationCode();
      });
      $('#copyCodeBt').on('click', function(event){
        var linkText  = document.location.origin
            linkText += '/auth?token='  
            linkText += $('#generateCodeProgress input').val()
        copyTextToClipboard(linkText)
        $('#copyCodeBt').text('Copied!')
      })
    } 
    function activateCodeField () {
        $('#generateCodeProgress').addClass('loading')
        $('#generateCodeProgress i').addClass('search')
    }
    function deActivateCodeField () {
        $('#generateCodeProgress').removeClass('loading')
        $('#generateCodeProgress i').removeClass('search')
    }
    function getInvitationCode () {
      var url = document.location.origin 
          url += '/' + 'invitation/' + 'get-code'
      var data = {
      }
      $.ajax({
        type: "POST",
        url: url,
        data: data,
      }).done(function (response) {
        console.log(response.result)
        if(response.result == 'OK'){
          $('#generateCodeProgress input').val(response.data.code)
          $('#generateCodeBt').hide()
          $('#copyCodeBt').show()
        } else {
          $('#generateCodeProgress input').val('Invitation error')
        }
        deActivateCodeField()
      }).fail(function () {
        $('#generateCodeProgress input').val('Code unavailable')
        deActivateCodeField()
      });
    }



  ///////////////
  // Copy to clipboard utility
  // taken from https://stackoverflow.com/questions/400212/how-do-i-copy-to-the-clipboard-in-javascript
  ///////////////
  function fallbackCopyTextToClipboard(text) {
    var textArea = document.createElement("textarea");
    textArea.value = text;

    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";

    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      var successful = document.execCommand('copy');
      var msg = successful ? 'successful' : 'unsuccessful';
      console.log('Fallback: Copying text command was ' + msg);
    } catch (err) {
      console.error('Fallback: Oops, unable to copy', err);
    }

    document.body.removeChild(textArea);
  }
  function copyTextToClipboard(text) {
    if (!navigator.clipboard) {
      fallbackCopyTextToClipboard(text);
      return;
    }
    navigator.clipboard.writeText(text).then(function() {
      console.log('Async: Copying to clipboard was successful!');
    }, function(err) {
      console.error('Async: Could not copy text: ', err);
    });
  }

  ///////////////
  });
</script>
