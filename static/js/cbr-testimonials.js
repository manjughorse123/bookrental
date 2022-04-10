$(function () {
	$('.testimonial-body').click(function () {
		if ($('#testimonial-slides').attr('data-transinprog') === 'false') {
			testimonialClicked();
		}
	});
	$('#testimonial-bullets div').click(function () {
		if ($('#testimonial-slides').attr('data-transinprog') === 'false') {
			testimonialClicked($(this).index());
		}
	});
	//Start the interval
	setTimeout("$('.testimonial-body:visible').click();", testimonialInterval);

	//Only do for small screens (all 4 show comfortably on desktop, no need to slide)
	if (isMobile() || isTablet()) {
		$('.highlight-item').click(function () {
			if ($('#hp2-highlights').attr('data-transinprog') === 'false') {
				restartHighlightTimer();
				moveHighlight();
			}
		});
		//Start the interval
		setTimeout("$('.highlight-item:visible').click();", highlightInterval);
}
});

function transitionDiv(slideSelector, bulletSelector, targetIndex, effect, effectTime) {   //Effect options: 'fade' or 'slide'
	$(slideSelector).parent().attr('data-transinprog', 'true');
	var visibleDiv = $(slideSelector + ':visible');
	var visibleIndex = $(visibleDiv).index();
	var maxIndex = $(slideSelector).last().index();
	var minIndex = 0;
	var indexToShow;

	var transSettingsIn;
	var transSettingsOut;
	if (effect === 'slide') {
		transSettingsIn = { direction: 'left' };
		transSettingsOut = { direction: 'right' };
	} else if (effect === 'fade') {
		transSettingsIn = 'swing';
		transSettingsOut = 'swing';
	}

	$(visibleDiv).hide(effect, transSettingsIn, effectTime, function () {
		if (!isNaN(parseInt(targetIndex)))   //Specific bullet clicked
			indexToShow = targetIndex;
		else
			indexToShow = visibleIndex + 1;

		if (indexToShow < minIndex || indexToShow > maxIndex)
			indexToShow = minIndex;

		var adjustZeroToOneBased = 1;
		$(slideSelector + ':nth-child(' + (indexToShow + adjustZeroToOneBased) + ')')
			.show(effect, transSettingsOut, effectTime, function () {
				$(slideSelector).parent().attr('data-transinprog', 'false');
			});

		if (bulletSelector != null && bulletSelector !== undefined) {
			$(bulletSelector).removeClass('selected');
			$(bulletSelector + ':nth-child(' + (indexToShow + adjustZeroToOneBased) + ')').addClass('selected');
		}
	});
}

var testimonialTimer;
var testimonialInterval = 6000;
var testimonialFade = 1000;
function testimonialClicked(index) {
	restartTestimonialTimer();
	moveTestimonial(index);
}
function moveTestimonial(index) {
	transitionDiv('.testimonial-body', '#testimonial-bullets div', index, 'fade', testimonialFade);
}
function restartTestimonialTimer() {   //Allows manual customer click to restart the slide timer
	clearInterval(testimonialTimer);
	testimonialTimer = setInterval(function () {
		moveTestimonial();
	}, testimonialInterval);
}