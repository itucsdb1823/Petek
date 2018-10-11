<template>
    <v-alert dismissible error @input="onClose" :value="true">
        {{ text }}
    </v-alert>
</template>

<script>
    export default {
        props: ['text'],
        name: "Alert",
        methods: {
            onClose () {
              this.$emit('dismissed')
            }
        }
    }
</script>

<style scoped>

</style>
