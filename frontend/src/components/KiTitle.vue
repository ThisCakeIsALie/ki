<template>
    <header class="container">
        <img src="../assets/plant.png">
        <div>
            <span class="title-text">Ki.</span>
            <span class="title-text small-text">Pronounciation tool.</span>
        </div>
    </header>
</template>

<script>

export default {
    name: 'ki-title'
}
</script>

<style scoped>
    .container {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    img {
        width: 2.5em;
        max-height: 2.5em;
        margin-right: 0.5em;
    }

    .title-text {
        display: block;
        color: gray;
    }

    .small-text {
        font-size: 0.7em;
    }
</style>