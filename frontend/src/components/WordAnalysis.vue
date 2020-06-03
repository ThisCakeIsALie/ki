<template>
    <ul class="fa-ul">
        <li><font-awesome-icon class="fa-li" icon="landmark" />
            In romanji that is...
            <span class="centered">{{ romanji }}</span>
        </li>
        <li><font-awesome-icon class="fa-li" icon="comment" />
            In English that sounds like...
            <span class="centered">{{ phoneticApprox }}</span>
        </li>
        <li><font-awesome-icon class="fa-li" icon="pen" />
            And it is written similarly to...
            <span class="centered">{{ syntacticApprox }}</span>
        </li>
    </ul>
</template>

<script>
const SEPARATOR = '·';

export default {
    name: 'word-analysis',
    props: [ 'data' ],
    computed: {
        romanji() {
            return this.data.syllables.join(SEPARATOR);
        },
        phoneticApprox() {
            return this.data.phonetic_approx.words.join(SEPARATOR);
        },
        syntacticApprox() {
            return this.data.syntactic_approx.words.join(SEPARATOR);
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