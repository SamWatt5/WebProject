import { useMediaQuery } from "@vueuse/core";
import { computed, reactive } from "vue";
import yaml from "yaml";

export const useIsMobile = () => {
  const MOBILE_BREAKPOINT = 768;
  const isMobile = useMediaQuery(`(max-width: ${MOBILE_BREAKPOINT -1}px)`);

  return isMobile.value;
}