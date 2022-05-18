/**
    Custom helpers for Holons front concept
    This script relies on Semantic UI js and jQuery, god bless its soul
*/

function setTabs() {
    $('.secondary.pointing.menu .item').tab();
}

function setTabAnimations() {
    $('.secondary.pointing.menu .item').click(function(){
         $('.tabs-wrapper').addClass('loading');
    });
    function transEnd(e) {
        var el = $(e.target);
        if ( el.hasClass('tabs-wrapper') ) {
            $('.tabs-wrapper').removeClass('loading');
        }
    }
    $('.tabs-wrapper').on('webkitTransitionEnd transitionend', function(e){
        setTimeout(function() {
            transEnd(e);
        }, 250);
    });
}
