<template>
    <div class="loans-deposits" style="margin:2rem">
        <div class="ui grid">
            <div class="eight wide column payroll">
                <h2>payroll</h2>

                <p class="muted">these are read-only stats used in cash flow and P&L.
                Use <a class="hm link" href="/people">people</a> to actually manage payroll</p>

                <p><b>last month total: $XXX,XXX</b></p>
                <p><b>this month:</b></p>

                <!--
                    what types can we have here?
                    1. salary
                    2. hourly
                    3. fixed variables (e.g. Warren logging $5 per 1k words) -->

                <div style="padding-left:2rem;border-bottom:30px solid #23272B">

                    <table class="hm table">
                        <tr>
                        <td>Salaries due:</td>
                        <td>$XXX,XXX</td>
                        </tr>
                        <tr>
                        <td>Hourly commitments so far:</td>
                        <td>$XXX,XXX</td>
                        </tr>
                        <tr>
                        <td>Fixed price commitments so far:</td>
                        <td>$XXX,XXX</td>
                        </tr>
                        <tr>
                        <td>Per unit commitments so far:</td>
                        <td>$XXX,XXX</td>
                        </tr>

                        <br><br>

                        <tr>
                        <td>subtotal</td>
                        <td>$XXX,XXX</td>
                        </tr>
                    </table>

                </div>

                <!--1. marketing budgets
                2. one-off expenses
                ?? should we just log it manually now to appear on cashflow balance?

                sup w/ one-off expenses?
                well, manual entries are dummed to failure, untill it's
                charged on the account directly.

                for that we need card issuing, huh?
                -->
            </div>
            <div class="eight wide column costs">
                <h2>variable costs {{ billingPeriodName }}</h2>

                <a @click="() => { editVariableCost = {new: true, context_id: activeContext.id, tags: []} }" style="width:100%" class="ui basic button">+ log new entry</a>

                <table class="hm table">
                <!-- what - payment date - amount - tag -->
                    <tbody>
                        <VariableCost
                            v-for="cost in activeVariableCosts" 
                            :key="cost.id"
                            :cost="cost"
                        ></VariableCost>
                    </tbody>
                </table>

                <h2>fixed costs</h2>
                <p>monthly reccuring costs</p>

                <a @click="() => { editFixedCost = {new: true, context_id: activeContext.id, tags: []} }" style="width:100%" class="ui basic button">+ log new entry</a>

                <table class="hm table">
                <!-- what - amount - tag -->
                    <tbody>
                        <FixedCost 
                            v-for="cost in activeFixedCosts" 
                            :key="cost.id"
                            :cost="cost"
                        ></FixedCost>
                    </tbody>
                </table>

            </div>
        </div>

        <FixedCostModal :toEdit="editFixedCost"></FixedCostModal>
        <VariableCostModal :toEdit="editVariableCost"></VariableCostModal>
        <BillingPeriodPicker></BillingPeriodPicker>
    </div>
</template>

<script>
import BillingPeriodPicker from './BillingPeriodPicker.vue'
import FixedCost from './FixedCost.vue'
import FixedCostModal from './FixedCostModal.vue'
import VariableCost from './VariableCost.vue'
import VariableCostModal from './VariableCostModal.vue'

export default {
    name: 'LoansDepositsComponent',

    components: {
        FixedCostModal,
        VariableCostModal,
        FixedCost,
        VariableCost,
        BillingPeriodPicker
    },

    props: {},

    data() {
        return {
            variableCosts: [],
            fixedCosts: [],

            tags: [],

            editFixedCost: null,
            editVariableCost: null,

            billingPeriodStart: new Date(),
            billingPeriodEnd: new Date(),
            billingPeriodName: ''
        }
    },
    computed: {
        now(){
            return (new Date())
        },
        apiUrl() {
            return window.location.origin + '/api/moneta'
        },

        activeContext(){
            return this.$parent.activeContext
        },
        activeVariableCosts(){
            return this.variableCosts.filter(c => 
                this.activeContext && c.context_id == this.activeContext.id && new Date(c.date) >= this.billingPeriodStart && new Date(c.date) <= this.billingPeriodEnd
            )
        },
        activeFixedCosts(){
            return this.fixedCosts.filter(
                c => {
                    let s = (new Date(c.started_at))
                    s.setDate(1)
                    let f = null
                    if(c.finished_at){
                        f = (new Date(c.finished_at))
                        f.setMonth(f.getMonth() + 1)
                        f.setDate(0)
                    }
                    return (
                        this.activeContext && 
                        c.context_id == this.activeContext.id &&
                        !(  
                            (s > this.billingPeriodEnd) || 
                            (f && f < this.billingPeriodStart)
                        ) 
                    )
                }
            )
        },
        activeTags(){
            return this.tags.filter(t => this.activeContext && t.context_id == this.activeContext.id)
        },

        totalVariable(){
            return this.activeVariableCosts.reduce((a, c) => a + (c.amount ? c.amount : 0))
        },
        totalFixed(){
            return this.activeFixedCosts.reduce((a, c) => a + (c.amount ? c.amount : 0))
        },
        totalCosts(){
            return this.totalFixed + this.totalVariable
        }
    },
    methods: {
        getVariableCosts(){
            fetch(this.apiUrl + '/variable-costs')
            .then(res => res.ok && res.json())
            .then(res => {
                if(!res) return

                this.variableCosts.length = 0
                this.variableCosts.push(...res)
                this.$forceUpdate()
            })
        },
        getFixedCosts(){
            fetch(this.apiUrl + '/fixed-costs')
            .then(res => res.ok && res.json())
            .then(res => {
                if(!res) return

                this.fixedCosts.length = 0
                // this.fixedCosts.push(...res.filter(fc => !this.fixedCosts.find(c => c.id == fc.id)))
                this.fixedCosts.push(...res)
                this.$forceUpdate()
            })
        },
        getTags(){
            fetch(this.apiUrl + '/tags')
            .then(res => res.ok && res.json())
            .then(res => {
                if(!res) return

                // this.tags.push(...res.filter(t => !this.tags.find(existedT => existedT.id == t.id)))
                this.tags.length = 0
                this.tags.push(...res)
                this.$forceUpdate()
            })
        },

        /**
         * @param {Date} date
         */
        formatDate(date){
            if(typeof(date) != 'object') date = new Date(date)

            const formater = Intl.DateTimeFormat('en', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            })

            return formater.format(date)
        },
        getCookie(name){
            let matches = document.cookie.match(new RegExp(
                "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
            ));
            return matches ? decodeURIComponent(matches[1]) : undefined;
        },
    },
    mounted() {
        this.getTags()
        this.getVariableCosts()
        this.getFixedCosts()

        this.billingPeriodStart = new Date(this.now.getFullYear(), this.now.getMonth(), 1)
        this.billingPeriodEnd = new Date(this.now.getFullYear(), this.now.getMonth() + 1, 0)

        const costsEl = document.querySelector('.costs')
        const payrollEl = document.querySelector('.payroll')

        if(costsEl && payrollEl){
            costsEl.style.height = payrollEl.offsetHeight + 'px'
        }
        
    },
}
</script>

<style>
.costs{
    overflow: auto;
}
.cost-tag,
.ti-tag.ti-valid{
    /* tag styling */
    margin: 0 2px !important;
    padding: 3px !important;
    background-color: rgba(0,0,0,.05) !important;
    border-radius: 2px !important; 
    color: unset !important;
}
.ti-input, 
.costs input{
    /* inputs styling here */
    font-size: 14px;
    padding: 4px;
    outline: none;
}
.ti-input:focus, 
.costs input:focus{
    outline: none;
}
</style>