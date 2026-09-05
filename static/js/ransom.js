(function () {
    var ALL_FONTS = ['rf-1', 'rf-2', 'rf-3', 'rf-4', 'rf-5', 'rf-6', 'rf-7', 'rf-8', 'rf-9', 'rf-10'];
    var CHIPS = ['chip-ink', 'chip-navy', 'chip-blue', 'chip-sky', 'chip-paper', 'chip-outline', null];
    var INKS = ['ink-black', 'ink-navy', 'ink-blue', 'ink-slate'];

    function rand(arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    }

    function randRange(min, max) {
        return Math.random() * (max - min) + min;
    }

    function randomizeLetter(span, mode) {
        span.className = 'letter';
        span.classList.add(rand(ALL_FONTS));

        var subtle = mode === 'ink';
        var rotate = subtle ? randRange(-5, 5) : randRange(-12, 12);
        var rise = subtle ? randRange(-2, 2) : randRange(-6, 6);
        var scale = subtle ? randRange(0.95, 1.05) : randRange(0.85, 1.15);
        span.style.transform = 'rotate(' + rotate.toFixed(1) + 'deg) translateY(' + rise.toFixed(1) + 'px) scale(' + scale.toFixed(2) + ')';
        span.style.margin = '0 0.01em';

        if (mode === 'chips') {
            var chip = rand(CHIPS);
            if (chip) span.classList.add(chip);
        } else if (mode === 'ink') {
            span.classList.add(rand(INKS));
        }
    }

    function buildLetters(el, mode) {
        var text = el.dataset.text || el.textContent;
        if (!el.dataset.text) el.dataset.text = text;
        el.setAttribute('aria-label', text);
        el.innerHTML = '';

        // Group letters per word inside an atomic wrapper span, so the
        // browser can only wrap lines between words (like normal text),
        // never in the middle of a word.
        var words = text.split(' ');
        words.forEach(function (word, wi) {
            var wordSpan = document.createElement('span');
            wordSpan.className = 'word';

            Array.from(word).forEach(function (char) {
                var span = document.createElement('span');
                span.className = 'letter';
                span.setAttribute('aria-hidden', 'true');
                span.textContent = char;
                randomizeLetter(span, mode);
                span.addEventListener('mouseenter', function () {
                    randomizeLetter(span, mode);
                });
                wordSpan.appendChild(span);
            });

            el.appendChild(wordSpan);
            if (wi < words.length - 1) {
                el.appendChild(document.createTextNode(' '));
            }
        });
    }

    function initRansomText() {
        document.querySelectorAll('.ransom-text.ransom-chips').forEach(function (el) {
            buildLetters(el, 'chips');
        });
        document.querySelectorAll('.ransom-text.ransom-ink').forEach(function (el) {
            buildLetters(el, 'ink');
        });
    }

    document.addEventListener('DOMContentLoaded', initRansomText);
})();
