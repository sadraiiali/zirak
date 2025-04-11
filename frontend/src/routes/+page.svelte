<!-- In your parent Svelte component -->
<script>
	import MetadataDisplay from '$lib/components/MetadataDisplay.svelte';

	// Example data (can be dynamic)
	const myTags = [
        { text: '#Svelte', color: 'purple' },
        { text: '#WebApp', color: 'blue' },
    ];
    const requestTime = new Date(2024, 5, 15, 10, 30, 0); // Example date
    const intentValue = "Analyze Sentiment";
    const modelPref = "Balanced";

</script>

<!-- Pass props to the component -->
<MetadataDisplay
	tags={myTags}
	intent={intentValue}
	modelPreference={modelPref}
	requestTimestamp={requestTime}
/>
