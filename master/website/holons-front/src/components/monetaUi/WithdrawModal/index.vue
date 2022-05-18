<template>
    <div class="hm modal">
        <div class="content">
            <compontent :is="paymentSystemCompontent"></compontent>
        </div>
    </div>
</template>

<script>
import StripeModalContent from './StripeModalContent'
import PaysendModalContent from './PaysendModalContent' 
import DefaultModalContent from './DefaultModalContent' 

export default {
    name: 'WithdrawModal',
    components: {
        StripeModalContent,
        PaysendModalContent,
        DefaultModalContent
    },
    data() {
        return {
            paymentAccount: {},
            countries: []
        }
    },
    computed: {
        apiUrl(){
            return window.location.origin + '/api/moneta'
        },
        paymentSystemCompontent(){
            return this.paymentAccount.payment_system ? this.paymentAccount.payment_system + 'ModalContent' : 'DefaultModalContent'
        }
    },
    mounted() {
        fetch(this.apiUrl + '/withdraw')
        .then(res =>  res.text())
        .then(res => {
            try {
                res = JSON.parse(res)
            } catch(err) {
                console.log(err)
                res = {}
            }

            if(!res.success) return console.log('Error while loading withdraw information: ' + res.message)

            this.paymentAccount = res.account
        })

        if(document.querySelector('#withdraw-modal-open')){
            document.querySelector('#withdraw-modal-open').onclick = (evt) => {
                evt.stopPropagation()
                evt.preventDefault()
                this.$el.classList.add('active')
            }
        }
    }
}
</script>