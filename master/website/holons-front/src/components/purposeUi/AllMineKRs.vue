<template>
    <div class="all-mine-purposes">
        <div class="kr-in-list" v-for="kr in keyResults.filter(kr => kr.purpose.status == filter).sort(KRSortFn)" :key="kr.id">
            <h3>{{ kr.purpose.title }} - <a :href="`/purpose/?purposeId=${kr.purpose.id}`">see purpose</a></h3>
            <h5>KR: {{ kr.title }}</h5>
            <div>Context: {{ kr.context.foreign.name == me.handle ? 'professional' : kr.context.foreign.name }}</div>
            <div>Season status: {{ kr.purpose.status }}</div>
            <div v-if="kr.purpose.start_at">Season start: {{ formatDate(new Date(kr.purpose.start_at)) }}</div>
            <hr>
            <div>Fact: {{ kr.current_value }}</div>
            <div>Plan: {{ kr.target_value }}</div>
            <div v-if="kr.next_check_in">Next check in: {{ formatDate(new Date(kr.next_check_in.date)) }}</div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'AllMineKRs',
    props:{
        filter: {
            required: false
        }
    },
    data(){
        return {
            keyResults: [],
            me: {
                handle: window.handle   
            }
        }
    },
    computed: {
        apiUrl(){
            return window.location.origin + '/api/purpose'
        }
    },
    methods : {
        KRSortFn(a, b){
            if(a.purpose.status == b.purpose.status){
                return new Date(b.purpose.start_at) - new Date(a.purpose.start_at)
            }else if(a.purpose.status == 'finish'){
                return 1
            }else{
                return -1
            }
        },
        formatDate(date){
            return Intl.DateTimeFormat('en', { day: '2-digit', month: '2-digit', year: 'numeric' }).format(new Date(date))
        }
    },
    mounted(){
        fetch(this.apiUrl + '/keyresults')
        .then(res => res.ok && res.json())
        .then(res => {
            if(!res) return

            this.keyResults = res

            this.$forceUpdate()
        })
        .catch(err => console.log('Err while loading purposes: ' + err))
    },
    beforeUpdate(){
        if(this.filter == 'current'){
            this.filter = 'start'
        }
    }
}
</script>

<style scoped>
.kr-in-list{
    padding: 10px;
    margin: 10px 0;
    border: 1px black solid;
    border-radius: 5px;
}
</style>