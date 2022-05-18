<template>
    <div class="stripe-payment">
        <h5>type card to use <a href="https://paysend.com">Paysend</a></h5>
        <input 
            type="text"
            v-model="$parent.paymentAccount.card_number"
            @change="saveCard"
            @input="cardRestrictions"
            maxlength="19" 
        >
    </div>
</template>

<script>

export default {
    methods: {
        getCookie(name){
            let matches = document.cookie.match(new RegExp(
                "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
            ));
            return matches ? decodeURIComponent(matches[1]) : undefined;
        },
        cardRestrictions(){
            this.$parent.paymentAccount.card_number = this.$parent.paymentAccount.card_number.replace(/\D/gi, '')
        },
        saveCard(){
            fetch(this.$parent.apiUrl + '/withdraw/', {
                method: 'PATCH',
                body: JSON.stringify({
                    card_number: this.$parent.paymentAccount.card_number
                }),
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken')
                }
            })
        }
    }
}
</script>

<style scoped>
h5 a{
    font-family: inherit !important;
}
</style>