<script lang="ts">
    import { ListTree } from "@lucide/svelte";

    type Step = {
        id: number | string; // Unique identifier for the step
        title: string; // The display name of the step
        // Add other potential properties if needed, e.g., description
    };

    type Props = {
        strategyName: string; // The name of the AI strategy being used
        steps: Step[]; // An array of steps involved in the strategy
    };

    // Define props using Svelte 5 runes
    let { strategyName, steps }: Props = $props();
</script>

<div class="strategy-display-wrapper">
    <h3 class="strategy-title gap-1">
        <!-- Use the Lucide Svelte component -->
        <ListTree class="icon" size={16} strokeWidth={2} />
        Strategy Used: <span class="strategy-name">{strategyName}</span>
    </h3>
    <ol class="strategy-steps ">
        {#each steps as step (step.id)}
            <li class="pl-1">{step.title}</li>
        {/each}
    </ol>
</div>

<style>
    .strategy-display-wrapper {
        /* Original: mb-5 border border-border bg-gradient-to-br from-muted/30 to-muted/60 rounded-lg p-4 shadow-sm */
        margin-bottom: 1.25rem; /* mb-5 */
        border: 1px solid hsl(var(--border)); /* border border-border */
        background-image: linear-gradient(
            to bottom right,
            hsl(var(--muted) / 0.3),
            /* from-muted/30 */ hsl(var(--muted) / 0.6) /* to-muted/60 */
        );
        border-radius: var(--radius); /* rounded-lg */
        padding: 1rem; /* p-4 */
        box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05); /* shadow-sm */
        overflow: hidden; /* Ensure gradient stays within bounds */
    }

    .strategy-title {
        /* Original: text-sm font-semibold text-foreground mb-2 flex items-center */
        font-size: 0.875rem; /* text-sm */
        line-height: 1.25rem; /* text-sm */
        font-weight: 600; /* font-semibold */
        color: hsl(var(--foreground)); /* text-foreground */
        margin-bottom: 0.5rem; /* mb-2 */
        display: flex;
        align-items: center;
    }

    .strategy-title .icon {
        /* Original: w-4 h-4 mr-2 text-primary */
        /* Size set via prop */
        margin-right: 0.5rem; /* mr-2 */
        color: hsl(var(--primary)); /* text-primary */
        flex-shrink: 0; /* Prevent icon shrinking */
    }

    .strategy-name {
        /* Original: ml-1.5 font-semibold text-primary */
        margin-left: 0.375rem; /* ml-1.5 */
        font-weight: 600; /* font-semibold */
        color: hsl(var(--primary)); /* text-primary */
    }

    .strategy-steps {
        /* Original: list-decimal list-inside text-xs text-muted-foreground space-y-1 pl-1 */
        list-style-type: decimal; /* list-decimal */
        list-style-position: inside; /* list-inside */
        font-size: 0.75rem; /* text-xs */
        line-height: 1rem; /* text-xs */
        color: hsl(var(--muted-foreground)); /* text-muted-foreground */
        padding-left: 0.25rem; /* pl-1 */
        margin-top: 0; /* Reset default ol margin */
        margin-bottom: 0; /* Reset default ol margin */
    }

    .strategy-steps li + li {
        /* Original: space-y-1 */
        margin-top: 0.25rem; /* space-y-1 */
    }
</style>
