<template>
    <div>
        <input type="text" v-model="searchValue" @input="handleInput()">
        <button @click="submitSearch(searchValue)">
            <font-awesome-icon icon="search" />
        </button>
    </div>
</template>

<script>
export default {
    name: 'search-bar',
    data() {
        return {
            searchValue: ''
        };
    },
    methods: {
        handleInput() {
            if (this.timeout) {
                clearTimeout(this.timeout);
            }

            this.timeout = setTimeout(() => {
                this.submitSearch(this.searchValue);
            }, 250);
        },
        submitSearch(query) {
            this.$emit('search', query);
        }
    }
}
</script>

<style scoped>
    div {
        border-bottom: 1px solid gray;
        display: flex;
        flex-wrap: nowrap;
    }

    input {
        font-size: 1em;
        border: none;
        width: 90%;
    }

    button {
        font-size: 1em;
        border: none;
        background: none;
        width: 10%;
    }
</style>
