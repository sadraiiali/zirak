<script>
    import { Tag, Zap, Settings2, CalendarClock } from "@lucide/svelte";

    /**
     * @typedef {{ text: string; color: 'blue' | 'green' | 'purple' | string }} TagItem
     * @type {TagItem[]}
     */
    let {
        tags = [
            { text: "#AI", color: "blue" },
            { text: "#Mastodon", color: "green" },
            { text: "#OpenSource", color: "purple" },
        ],
        intent = "Generate Toot",
        modelPreference = "Default Creative",
        requestTimestamp = new Date(),
    } = $props();

    const colorClasses = {
        blue: "tag-blue",
        green: "tag-green",
        purple: "tag-purple",
        // Add more colors as needed or handle custom hex/rgb codes
    };

    function formatTimestamp(ts) {
        if (!ts || !(ts instanceof Date)) {
            return "N/A";
        }
        try {
            return ts.toLocaleString([], {
                dateStyle: "short",
                timeStyle: "short",
            });
        } catch (e) {
            console.error("Error formatting timestamp:", e);
            return "Invalid Date";
        }
    }
</script>

<div class="metadata-container">
    <h3 class="metadata-title">Metadata</h3>
    <div class="metadata-box">
        <div class="metadata-item">
            <Tag class="icon" size={14} />
            Tags:
            <span class="tags-wrapper">
                {#each tags as tag (tag.text)}
                    <span class="tag {colorClasses[tag.color] || ''}"
                        >{tag.text}</span
                    >
                {/each}
            </span>
        </div>
        <div class="metadata-item">
            <Zap class="icon" size={14} />
            Intent: <span class="metadata-value">{intent}</span>
        </div>
        <div class="metadata-item">
            <Settings2 class="icon" size={14} />
            Model Preference:
            <span class="metadata-value">{modelPreference}</span>
        </div>
        <div class="metadata-item">
            <CalendarClock class="icon" size={14} />
            Requested:
            <span class="metadata-value"
                >{formatTimestamp(requestTimestamp)}</span
            >
        </div>
    </div>
</div>

<style>
    /* Define CSS Variables used in this component (or assume they are global) */
    :host {
        --muted-foreground: hsl(215.4 16.3% 46.9%);
        --foreground: hsl(222.2 84% 4.9%);
        --border: hsl(214.3 31.8% 91.4%);
        --background: hsl(0 0% 100%);
        --radius-md: calc(0.5rem - 2px); /* from .rounded-md */

        /* Tag Colors (Approximations from Tailwind) */
        --tag-blue-bg: #dbeafe; /* blue-100 */
        --tag-blue-text: #1e40af; /* blue-800 */
        --tag-green-bg: #d1fae5; /* green-100 */
        --tag-green-text: #065f46; /* green-800 */
        --tag-purple-bg: #ede9fe; /* purple-100 */
        --tag-purple-text: #5b21b6; /* purple-800 */
    }

    .metadata-container {
        padding-top: 0.5rem; /* pt-2 */
    }
    /* space-y-2 */
    .metadata-container > * + * {
        margin-top: 0.5rem;
    }

    .metadata-title {
        font-size: 0.75rem; /* text-xs */
        line-height: 1rem;
        font-weight: 600; /* font-semibold */
        color: var(--muted-foreground); /* text-muted-foreground */
        text-transform: uppercase; /* uppercase */
        letter-spacing: 0.05em; /* tracking-wider */
        margin-bottom: 0.5rem; /* Implicit from parent space-y */
    }

    .metadata-box {
        font-size: 0.75rem; /* text-xs */
        line-height: 1rem;
        color: var(--muted-foreground); /* text-muted-foreground */
        border: 1px solid var(--border); /* border border-border */
        border-radius: var(--radius-md); /* rounded-md */
        padding: 0.75rem; /* p-3 */
        background-color: rgba(
            255,
            255,
            255,
            0.5
        ); /* bg-background/50 assumes background is white */
    }
    /* space-y-1.5 */
    .metadata-box > * + * {
        margin-top: 0.375rem;
    }

    .metadata-item {
        display: flex; /* flex */
        align-items: center; /* items-center */
    }

    .icon {
        width: 0.875rem; /* w-3.5 */
        height: 0.875rem; /* h-3.5 */
        margin-right: 0.375rem; /* mr-1.5 */
        flex-shrink: 0; /* flex-shrink-0 */
        stroke-width: 2; /* default stroke width */
        color: currentColor; /* Inherit color from parent */
    }

    .tags-wrapper {
        margin-left: 0.375rem; /* ml-1.5 */
        display: flex; /* flex */
        flex-wrap: wrap; /* flex-wrap */
        gap: 0.25rem; /* gap-1 */
    }

    .tag {
        display: inline-flex; /* inline-flex */
        align-items: center; /* items-center */
        border-radius: 9999px; /* rounded-full */
        padding-left: 0.5rem; /* px-2 */
        padding-right: 0.5rem; /* px-2 */
        padding-top: 0.125rem; /* py-0.5 */
        padding-bottom: 0.125rem; /* py-0.5 */
        font-size: 0.75rem; /* text-xs */
        line-height: 1rem;
        font-weight: 500; /* font-medium */
        white-space: nowrap;
    }

    .tag-blue {
        background-color: var(--tag-blue-bg);
        color: var(--tag-blue-text);
    }
    .tag-green {
        background-color: var(--tag-green-bg);
        color: var(--tag-green-text);
    }
    .tag-purple {
        background-color: var(--tag-purple-bg);
        color: var(--tag-purple-text);
    }

    .metadata-value {
        margin-left: 0.375rem; /* ml-1.5 */
        font-weight: 500; /* font-medium */
        color: var(--foreground); /* text-foreground */
    }
</style>
