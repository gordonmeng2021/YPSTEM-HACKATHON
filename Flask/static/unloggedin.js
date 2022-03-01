/*//////////////////////
	*
	* SCROLLMAGIC STARTS
	*
	*//////////////////////
	// init controller
    var controller = new ScrollMagic.Controller();

    //flow
     $(".flow").each(function(){
       $(this).addClass('out');
       new ScrollMagic.Scene({
         triggerElement: this,
         triggerHook: 0,
         duration: 600
       })
       .on("enter", function(ev){$(ev.target.triggerElement()).removeClass('out');})
       .on("leave", function(ev){$(ev.target.triggerElement()).addClass('out');})
       .addTo(controller);
     });
   
    //fade
     $(".fade").each(function(){
       $(this).addClass('out');
       new ScrollMagic.Scene({
         triggerElement: this,
         triggerHook: 0.65
       })
       .on("enter", function(ev){$(ev.target.triggerElement()).removeClass('out');})
       .on("leave", function(ev){$(ev.target.triggerElement()).addClass('out');})
       .addTo(controller);
     });
   
   $('.container').removeClass('out');