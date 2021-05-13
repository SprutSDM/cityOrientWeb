<template>
    <v-app id="inspire">
        <router-view name="header"/>
        <v-main>
            <v-container style="height: 100%">
                <router-view></router-view>
            </v-container>
        </v-main>
    </v-app>
</template>
