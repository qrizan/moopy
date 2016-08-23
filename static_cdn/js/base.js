$(document).ready(function(){
    $(".content-markdown").each(function(){
        var content = $(this).text()
        var contentMarkdown = marked(content)
        $(this).html(contentMarkdown)
    })

    $(".content-markdown img").each(function(){
            $(this).addClass("ui fluid image")
    })

    var titleForm = $('#id_title');
    setTitle(titleForm.val())

    var descriptionForm = $('#id_description');
    setDescription(descriptionForm.val())

    titleForm.keyup(function() {
        var titleNew = $(this).val()
        setTitle(titleNew)
    })

    descriptionForm.keyup(function() {
        var descriptionNew = $(this).val()
        setDescription(descriptionNew)
    })

    function setDescription(value){
        var markedDescription = marked(value)
        $("#preview-description").html(markedDescription)
        $("#preview-description img").each(function(){
            $(this).addClass("ui fluid image")
        })
    }

    function setTitle(value){
        $("#preview-title").text(value)
    }


})
$('.ui.embed').embed();

$(".comment-reply-button").click(function(event){
    event.preventDefault();
    $(this).parent().next(".comment-reply").fadeToggle();
})