<template>
    
    <div id="costs-log-controls" class="ui secondary menu secondary-navigation">
        <a 
            v-for="shortcut in shortcuts" 
            :key="shortcut.name" 
            :class="[{'active': shortcut == activeShortcut}, 'item']"
            @click="() => changeShortcut(shortcut)"
        >
            {{ shortcut.name }}
        </a>
        <a class="item" style="opacity: .5;">
        [ custom date picker ]
        </a>
    </div>
</template>

<script>
export default {
    data() {
        return {
            shortcuts: [],
            activeShortcut: {}
        }
    },
    computed:{
        now(){
            return new Date()
        }
    },
    methods: {
        changeShortcut(shortcut){
            this.activeShortcut = shortcut

            this.$parent.billingPeriodStart = shortcut.start
            this.$parent.billingPeriodEnd = shortcut.end
            this.$parent.billingPeriodName= shortcut.name
        }
    },
    mounted(){
        this.shortcuts.push(
            {
                name: 'this month',
                start: new Date(this.now.getFullYear(), this.now.getMonth(), 1),
                end: new Date(this.now.getFullYear(), this.now.getMonth() + 1, 0)
            },
            {
                name: 'past month',
                start: new Date(this.now.getFullYear(), this.now.getMonth() - 1, 1),
                end: new Date(this.now.getFullYear(), this.now.getMonth(), 0)
            },
            {
                name: 'next month',
                start: new Date(this.now.getFullYear(), this.now.getMonth() + 1, 1),
                end: new Date(this.now.getFullYear(), this.now.getMonth() + 2, 0)
            },
            {
                name: 'this year',
                start: new Date(this.now.getFullYear(), 0, 0),
                end: new Date(this.now.getFullYear(), 11, 30)
            }
        )

        this.activeShortcut = this.shortcuts[0]
    }
}
</script>

<style scoped>
a{
    cursor: pointer !important;
}

#costs-log-controls{
    position: fixed;
    bottom: 20px;
    background: #fff;
    border: 1px solid #23272B !important;
    min-width: 73%;
}
</style>