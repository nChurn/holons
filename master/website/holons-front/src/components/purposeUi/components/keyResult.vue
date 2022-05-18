<template>
    <div class="key-result__single">

        <div class="flex">
            <div style="padding-left: 0">
                <img
                    :src="keyResult.owner ? keyResult.owner.userpic : keyResult.creator.userpic"
                    width="40px"
                    style="box-shadow: 2px 2px #23272B"
                />
            </div>
            <div>
                <h4>
                    {{ keyResult.title }}

                    <span v-if="purpose && purpose.status == 'draft'" style="font-size: 12px;padding: 15px;text-transform: uppercase">
                        <a class="hm link " @click.stop="() => { $parent.editKeyResult = keyResult }">edit</a> \
                        <a class="hm link" @click.stop="() => $parent.deleteKeyResult(keyResult)">
                            <i class="trash alternate outline icon"></i>
                        </a>
                    </span>
                </h4>
            </div>
            <div>
                <span class="objective__key-result-current-value" v-if="purpose && purpose.status != 'draft'">
                    {{ keyResult.type.name.toLowerCase() == 'yes/no' ? keyResult.current_value ? 'Yes' : 'No' : keyResult.current_value }}
                </span>
                <span v-if="keyResult.type.name.toLowerCase() == 'percentage'">%</span>
            </div>
            <div>
                <span class="objective__key-result-target-value">
                    {{ keyResult.type.name.toLowerCase() == 'yes/no' ? keyResult.target_value ? 'Yes' : 'No' : keyResult.target_value }}
                </span>
                <span v-if="keyResult.type.name.toLowerCase() == 'percentage'">%</span>
            </div>
        </div>
        <!-- logs
            1. output all ( intervals ) before season due date i.e.
            1.1. output placeholders
            1.2. output existing logs 
        -->
        <div class="kr-logs" v-if="purpose.status != 'draft'">
            <!-- <div class="kr-logs__item placeholder flex">
                <span class="number">12</span>
            </div>
            <div class="kr-logs__item placeholder flex">
                <span class="number">11</span>
            </div>
            <div class="kr-logs__item placeholder flex">
                <span class="number">10</span>
            </div>
            <div class="kr-logs__item placeholder flex">
                <span class="number">9</span>
            </div>
            <div class="kr-logs__item placeholder flex">
                <span class="number">8</span>
            </div>
            <div class="kr-logs__item placeholder flex">
                <span class="number">7</span>
            </div>
            <div class="kr-logs__item placeholder flex">
                <span class="number">6</span>
            </div>
            <div class="kr-logs__item placeholder flex">
                <span class="number">5</span>
            </div>
            <div class="kr-logs__item placeholder flex">
                <span class="number">4</span>
                <div>
                plan for the week: do X
                </div>
            </div>

            <div class="kr-logs__item logged flex">
                <span class="number">3</span>
                <div>first campaigns went off first campaigns went off first campaigns went off
                first campaigns went off first campaigns went off first campaigns went off first
                campaigns went off first campaigns went off first campaigns went off first campaigns went off first campaigns went off first campaigns went off
                    first campaigns went off first campaigns went off first campaigns went off first
                    campaigns went off first campaigns went off first campaigns went off</div>
            </div>

            <div class="kr-logs__item logged flex">
                <span class="number">2</span>
                <div>work started</div>
            </div> -->

            <div class="kr-logs__item logged flex" v-for="(checkIn, i) in keyResult.check_ins.filter(ci => ci.date).sort(CISortFn)" :key="checkIn.id">
                <span class="number">{{ keyResult.check_ins.filter(ci => ci.date).length - i }}</span>
                <div>{{ checkIn.fact }}</div>
                <div>Date: {{ Intl.DateTimeFormat('en', { day: '2-digit', month: '2-digit', year: 'numeric' }).format(new Date(checkIn.date)) }}</div>
            </div>
        </div>  <!--kr-logs end-->
    </div>


</template>
<script>
export default {
    props: {
        keyResult: {
            type: Object
        }
    },
    data(){
        return {
            purpose: this.$parent.purpose
        }
    },
    computed: {
        isOwner(){
            return (
                !this.keyResult.owner && (
                    !this.keyResult.creator || 
                    this.keyResult.creator.user_id == window.user_id
                ) || 
                this.keyResult.owner.user_id == window.user_id
            )
        }
    },
    methods: {
        CISortFn(a, b){
            return (new Date(b.date) - new Date(a.date))
        }
    }
}
</script>
