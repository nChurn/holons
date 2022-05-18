<template>
    <tr>
        <td>
            <div class="ui dropdown icon item" >
                <i class="wrench icon"></i>
                <div @click.self="() => null" class="menu">
                    <div @click.self="function(){ $parent.editVariableCost = cost }" class="item">
                      edit
                    </div>
                    <div @click.self="deleteCost" class="item">
                      delete
                    </div>
                </div>
            </div>
        </td>
        <td>{{ cost.name }}</td>
        <td>${{ cost.amount }}</td>
        <td><span class="cost-tag" v-for="tag in cost.tags" :key="tag.id">{{ tag.name }}</span></td>
        <td>{{ $parent.formatDate(cost.date) }}</td>
    </tr>
</template>

<script>
export default {
    props:{
        cost: {
            type: Object,
            required: true
        }
    },
    methods: {
        deleteCost(){
            fetch(this.$parent.apiUrl + `/variable-costs/${this.cost.id}`, {
                method: 'DELETE',
                headers:{
                    'X-CSRFToken': this.$parent.getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(res => res.ok && res.json())
            .then(res => {
                if(!res) return

                this.$parent.getVariableCosts()
            })
        }
    },
    mounted(){
        $('.ui.dropdown').dropdown()
    }
}
</script>