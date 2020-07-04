<template>
    <ul class="fa-ul">
        <li><font-awesome-icon class="fa-li" icon="landmark" />
            In romanji that is...
            <span class="centered" v-html="romanji"></span>
        </li>
        <li><font-awesome-icon class="fa-li" icon="comment" />
            In English that sounds like...
            <span class="centered" v-html="phoneticApprox"></span>
        </li>
        <li><font-awesome-icon class="fa-li" icon="pen" />
            And it is written similarly to...
            <span class="centered" v-html="syntacticApprox"></span>
        </li>
    </ul>
</template>

<script>
const SEPARATOR = '·';
const COLORS = ['rgba(25, 165, 152, 1)', '#97bf9f', '#bec5ab'];

const correctedFloor = (number, precision = 15) => {
    const correctedNumber = parseFloat(number.toPrecision(precision));

    return Math.floor(correctedNumber);
};

const percentageSlice = (word, start, end) => {
    const startIdx = correctedFloor(word.length * start);
    const endIdx = correctedFloor(word.length * end);

    return word.slice(startIdx, endIdx);
};

const colorWheel = function*(colors) {
    while (true) {
        for (const color of colors) {
            yield color;
        }
    }
}

const displaySyllables = (syllables, approx = null) => {
    if (!approx) {
        return syllables.join(SEPARATOR);
    }

    const wheel = colorWheel(COLORS);

    const wholeWord = syllables.join('');

    const matchPercentages = approx.word_matched_percentages;

    let charColors = [];
    let lastPercentage = 0;

    matchPercentages.forEach(percentage => {
        const nextPercentage = lastPercentage + percentage;
        const coloredPart = percentageSlice(wholeWord, lastPercentage, nextPercentage);
        const partLength = coloredPart.length;

        const { value: color } = wheel.next();

        const newColors = Array(partLength).fill(color);

        charColors = charColors.concat(newColors);

        lastPercentage = nextPercentage;
    });

    
    const coloredSyllables = [];
    syllables.forEach(syllable => {
        let coloredSyllable = '';

        for (const char of syllable) {
            const nextColor = charColors.shift();
            const coloredChar = `<span style="color: ${nextColor}">${char}</span>`

            coloredSyllable += coloredChar;
        }

        coloredSyllables.push(coloredSyllable);
    });

    return coloredSyllables.join(SEPARATOR);
};

const colorApproxWord = (word, color) => {
    const coloredResult = `
        <span style="color: ${color};">${word}</span>
    `;

    return coloredResult;
};

const displayApprox = approx => {
    const { words } = approx;

    const wheel = colorWheel(COLORS);

    const coloredWords = [];

    words.forEach(word => {
        const { value: color } = wheel.next();

        const coloredWord = colorApproxWord(word, color);

        coloredWords.push(coloredWord);
    });

    return coloredWords.join(SEPARATOR);
};

export default {
    name: 'word-analysis',
    props: [ 'data' ],
    computed: {
        romanji() {
            return displaySyllables(this.data.syllables, this.data.phonetic_approx);
        },
        phoneticApprox() {
            const approx = this.data.phonetic_approx;

            return displayApprox(approx);
        },
        syntacticApprox() {
            const approx = this.data.syntactic_approx;

            return displayApprox(approx);
        }
    }
}
</script>

<style scoped>
    li {
        margin-bottom: 1em;
    }

    .centered {
        text-align: center;
        font-size: 1.5em;
        display: block;
        margin: 0.5em;
    }
</style>