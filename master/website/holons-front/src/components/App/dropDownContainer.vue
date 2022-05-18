<template lang="html">
    <div v-bind:class="{'drop-down-container': true, 'dd-minimized': minimized}">
        <slot></slot>
        <div class="drop-down-button" v-on:click="handleClick">
            {{buttonMessage}}
        </div>
    </div>
</template>

<script>

const buttonMessages = [
    "less",
    "..."
]

export default {
    name: 'DropDownContainer',

    data() {
        return {
            buttonMessage: buttonMessages[1],
            minimized: true
        }
    },

    methods: {
        handleClick: function() {
            this.minimized = !this.minimized;
            this.buttonMessage = buttonMessages[Number(this.minimized)];
        }
    }
}
</script>

<style scoped lang="css">
.drop-down-container {
    overflow: -moz-hidden-unscrollable;
    overflow: hidden;
}
.drop-down-container > .drop-down-button {
    text-align: center;
}
.drop-down-container > .drop-down-button:hover {
    background-color: antiquewhite;
    cursor: pointer;
    color: black;
}
</style>
