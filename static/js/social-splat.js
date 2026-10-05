(function () {
    var POINTS = 9;        // vertices for the main blob outline
    var SVG_NS = 'http://www.w3.org/2000/svg';

    function randRange(min, max) {
        return Math.random() * (max - min) + min;
    }

    var SPLAT_COLORS = [
        'hsl(355, 70%, 42%)', // red
        'hsl(28, 78%, 42%)',  // orange
        'hsl(48, 78%, 36%)',  // gold
        'hsl(140, 50%, 30%)', // green
        'hsl(185, 55%, 30%)', // teal
        'hsl(215, 60%, 42%)', // blue
        'hsl(265, 50%, 46%)', // purple
        'hsl(325, 60%, 42%)'  // magenta
    ];

    function randomSplatColor(tip) {
        var choices = SPLAT_COLORS.filter(function (c) { return c !== tip._lastColor; });
        var color = choices[Math.floor(Math.random() * choices.length)];
        tip._lastColor = color;
        return color;
    }

    function makeBlobPoints(w, h) {
        var cx = w / 2;
        var cy = h / 2;
        var rx = w * 0.5;
        var ry = h * 0.85;
        var pts = [];
        for (var i = 0; i < POINTS; i++) {
            var angle = (i / POINTS) * Math.PI * 2;
            var jitter = randRange(0.75, 1.25);
            pts.push([
                cx + rx * jitter * Math.cos(angle),
                cy + ry * jitter * Math.sin(angle)
            ]);
        }
        return pts;
    }

    function smoothClosedPath(pts) {
        var n = pts.length;
        var d = 'M ' + pts[0][0].toFixed(1) + ' ' + pts[0][1].toFixed(1) + ' ';

        for (var i = 0; i < n; i++) {
            var p0 = pts[(i - 1 + n) % n];
            var p1 = pts[i];
            var p2 = pts[(i + 1) % n];
            var p3 = pts[(i + 2) % n];

            var cp1x = p1[0] + (p2[0] - p0[0]) / 6;
            var cp1y = p1[1] + (p2[1] - p0[1]) / 6;
            var cp2x = p2[0] - (p3[0] - p1[0]) / 6;
            var cp2y = p2[1] - (p3[1] - p1[1]) / 6;

            d += 'C ' + cp1x.toFixed(1) + ' ' + cp1y.toFixed(1) + ', ' +
                        cp2x.toFixed(1) + ' ' + cp2y.toFixed(1) + ', ' +
                        p2[0].toFixed(1) + ' ' + p2[1].toFixed(1) + ' ';
        }
        return d + 'Z';
    }

    function setupTip(tip) {
        var text = tip.textContent;
        tip.textContent = '';

        var svg = document.createElementNS(SVG_NS, 'svg');
        svg.setAttribute('class', 'social-tip-splat');

        var path = document.createElementNS(SVG_NS, 'path');
        svg.appendChild(path);

        var label = document.createElement('span');
        label.className = 'social-tip-label';
        label.textContent = text;

        tip.appendChild(svg);
        tip.appendChild(label);

        var w = tip.offsetWidth || 100;
        var h = tip.offsetHeight || 40;
        svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);

        tip._splatBox = { w: w, h: h };
        tip._splatPath = path;
    }

    function showTip(tip) {
        var box = tip._splatBox;

        tip._splatPath.setAttribute('d', smoothClosedPath(makeBlobPoints(box.w, box.h)));
        tip._splatPath.setAttribute('stroke', randomSplatColor(tip));

        var dx = randRange(-10, 10);
        var dy = randRange(-6, 16);
        var rotate = randRange(-6, 6);

        tip.style.transform = 'translate(calc(-50% + ' + dx.toFixed(1) + 'px), ' + dy.toFixed(1) + 'px) rotate(' + rotate.toFixed(1) + 'deg) scale(1)';
        tip.classList.add('is-visible');
    }

    function hideTip(tip) {
        tip.classList.remove('is-visible');
        tip.style.transform = 'translate(-50%, 6px) scale(0.2)';
    }

    function initSocialSplat() {
        document.querySelectorAll('.social-tip').forEach(function (tip) {
            var wrap = tip.parentElement;
            if (!wrap) return;

            setupTip(tip);

            wrap.addEventListener('mouseenter', function () { showTip(tip); });
            wrap.addEventListener('mouseleave', function () { hideTip(tip); });
            wrap.addEventListener('focusin', function () { showTip(tip); });
            wrap.addEventListener('focusout', function () { hideTip(tip); });
        });
    }

    document.addEventListener('DOMContentLoaded', initSocialSplat);
})();
