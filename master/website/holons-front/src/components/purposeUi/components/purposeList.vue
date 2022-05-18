<template>
    <div class="purpose-list">
        <div class="purpose-list__cont">
            <div 
                v-for="purpose in purposes.reverse()" 
                :key="purpose.id" 
                :class="[`purpose-list_${purpose.status}`, 'purpose-list__purpose']"
                @click="() => $emit('select', purpose)" 
            >
                <h3 class="purpose-list__title">{{ purpose.title }}</h3>
                <div>{{ purpose.status }}</div>
                <div class="purpose-list__content">
                    <div>Objectives:</div>
                    <ol class="purpose-list__obj-list">
                        <li v-for="objective in purpose.objectives" :key="objective.id"><div class="purpose-list__obj">{{ objective.title }}</div></li>
                    </ol>
                </div>
            </div>
        </div>
        <!-- <div class="btns">
            <button @click="createPurpose" v-if="!purposes.filter(p => p.status != 'finish').length" class="button ui">new purpose</button>
        </div> -->
    </div>
</template>

<script>
export default {
    name: 'PurposeList',
    props: {
        purposes: {
            required: true
        }
    },
}
</script>

<style scoped>
.purpose-list__purpose{
    margin: 1.2rem 0;
    cursor: pointer;
}
.purpose-list__content{
    margin-left: 1rem;
}
.purpose-list__obj-list{
    margin-left: 1.5rem;
}
.purpose-list_draft{
    opacity: .7;
}
.purpose-list_start .purpose-list__title{
    text-decoration: underline;
}
</style>