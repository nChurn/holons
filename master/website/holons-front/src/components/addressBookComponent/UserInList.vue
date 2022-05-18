<template>
    <div :class="[{'me': item.handle == me}, 'v-autocomplete-user']">
        <span>{{ item.username || '' }}</span>&nbsp;
        <span style="opacity: .5;">{{ item.user_phone || '' }}</span>
    </div>
</template>

<script>
export default {
    props: {
        item: { 
            required: true,
            default: {
                username: '',
                user_phone: ''
            } 
        },
        searchText: { required: true }
    },
    data(){
        return {
            me: window.me
        }
    }
}
</script>

<style scoped>
.me *{
    font-weight: bold;
}
</style>