(function () {
    var POINTS = 12; // vertices in the blob — kept constant so CSS can
                      // smoothly interpolate from the closed dot to the splat

    function randRange(min, max) {
        return Math.random() * (max - min) + min;
    }

    // Builds a jittery blob polygon() around the tip's own center (50%,50%).
    // baseRadius/jitter are in percent of the element's box.
    function makeBlobPolygon(baseRadius, jitter) {
        var pts = [];
        for (var i = 0; i < POINTS; i++) {
            var angle = (i / POINTS) * Math.PI * 2;
            var r = Math.max(0, baseRadius + randRange(-jitter, jitter));
            var x = 50 + r * Math.cos(angle);
            var y = 50 + r * Math.sin(angle);
            pts.push(x.toFixed(1) + '% ' + y.toFixed(1) + '%');
        }
        return 'polygon(' + pts.join(', ') + ')';
    }

    function showTip(tip) {
        var dx = randRange(-10, 10);   // stay close to the icon horizontally
        var dy = randRange(-6, 16);    // can drift down and slightly over the icon
        var rotate = randRange(-6, 6);

        tip.style.transform = 'translate(calc(-50% + ' + dx.toFixed(1) + 'px), ' + dy.toFixed(1) + 'px) rotate(' + rotate.toFixed(1) + 'deg) scale(1)';
        tip.style.clipPath = makeBlobPolygon(46, 16);
        tip.classList.add('is-visible');
    }

    function hideTip(tip) {
        tip.classList.remove('is-visible');
        tip.style.transform = 'translate(-50%, 6px) scale(0.2)';
        tip.style.clipPath = makeBlobPolygon(2, 1);
    }

    function initSocialSplat() {
        document.querySelectorAll('.social-tip').forEach(function (tip) {
            var wrap = tip.parentElement;
            if (!wrap) return;

            wrap.addEventListener('mouseenter', function () { showTip(tip); });
            wrap.addEventListener('mouseleave', function () { hideTip(tip); });
            wrap.addEventListener('focusin', function () { showTip(tip); });
            wrap.addEventListener('focusout', function () { hideTip(tip); });
        });
    }

    document.addEventListener('DOMContentLoaded', initSocialSplat);
})();
