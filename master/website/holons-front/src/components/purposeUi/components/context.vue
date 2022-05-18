<template>
    <a :class="{active: isActive}" @click="() => $emit('select', context)" class="context item">
        {{ context.foreign.name }}
    </a>
</template>

<script>
export default {
    name: 'Context',
    props: {
        context: {
            type: Object,
            required: true
        },
        isActive: {
            type: Boolean
        }
    }
}
</script>
